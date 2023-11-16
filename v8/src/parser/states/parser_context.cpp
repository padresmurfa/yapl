#include "parser_context.hpp"

namespace org {
namespace yapllang {
namespace parser {
namespace states {

ParserContext::ParserContext(const lexer::tokenizer::TokenizerLine& line, std::vector<ParserState>& stateStack, std::vector<size_t> &indentation)
    : stateStack_(stateStack)
    , line_(line)
    , indentation_(indentation)
{
}

const size_t NUM_SPACES_PER_TAB = 4;

size_t lengthOfWhitespace(const std::string &whitespace) {
    size_t result = 0;
    for (auto c : whitespace) {
        if (c == '\t') {
            result += NUM_SPACES_PER_TAB;
        } else {
            result++;
        }
    }
    return result;
}

size_t ParserContext::getIndentLength() const
{
    size_t result = 0;
    for (auto i : indentation_) {
        result += i;
    }
    return result;
}

void ParserContext::indent(const std::string &newWhitespace)
{
    auto newWhitespaceLength = lengthOfWhitespace(newWhitespace);
    auto currentWhitespaceLength = getIndentLength();
    if (newWhitespaceLength <= currentWhitespaceLength) {
        throw exception("indenting to (" + std::to_string(newWhitespaceLength) + "), which is our prior indentation level (" + std::to_string(currentWhitespaceLength) + "), or less");
    }
    indentation_.push_back(newWhitespaceLength - currentWhitespaceLength);
}

int ParserContext::maybeDedent(const std::string &newWhitespace)
{
    if (!indentation_.empty()) {
        auto newWhitespaceLength = lengthOfWhitespace(newWhitespace);
        auto currentWhitespaceLength = getIndentLength();
        if (newWhitespaceLength > currentWhitespaceLength) {
            throw exception("expected a potential de-dent, found an in-dent instead");
        }

        int result = 0;
        while (!indentation_.empty() && getIndentLength() > newWhitespaceLength) {
            result++;
            indentation_.pop_back();
        }
        return result;
    }
    return 0;
}

bool ParserContext::wouldDedent(const std::string &newWhitespace) const {
    auto newWhitespaceLength = lengthOfWhitespace(newWhitespace);
    auto currentWhitespaceLength = getIndentLength();
    return currentWhitespaceLength > newWhitespaceLength;
}

bool ParserContext::wouldIndent(const std::string &newWhitespace) const {
    auto newWhitespaceLength = lengthOfWhitespace(newWhitespace);
    auto currentWhitespaceLength = getIndentLength();
    return newWhitespaceLength > currentWhitespaceLength;
}

const lexer::tokenizer::TokenizerLine &ParserContext::getCurrentLine() const
{
    return line_;
}

void ParserContext::pushOutputToken(const parser::ParserToken &token) {
    outputTokens_.push_back(token);
}

void ParserContext::push(ParserState state, const parser::ParserToken &token) {
    pushOutputToken(token);
    stateStack_.push_back(state);
}

void ParserContext::push(ParserState state) {
    stateStack_.push_back(state);
}

void ParserContext::pop(ParserState state, const parser::ParserToken &token) {
    pushOutputToken(token);
    pop(state);
}

bool ParserContext::emptyState() const {
    return stateStack_.empty();
}

void ParserContext::pop(ParserState expectedState) {
    if (stateStack_.empty()) {
        throw Exception(addContextToErrorMessage("ParserContext::pop went haywire: state-stack was empty"));
    }
    auto currentState = stateStack_.back();
    if (currentState != expectedState) {
        throw Exception(addContextToErrorMessage("ParserContext::pop went haywire: expected state-stack.top=" + to_string(expectedState) + ", but current state-stack.top=" + to_string(currentState)));
    }
    stateStack_.pop_back();
}

std::vector<parser::ParserToken> &ParserContext::mutateOutputTokens() {
    return outputTokens_;
}

const std::vector<parser::ParserToken> &ParserContext::getOutputTokens() {
    return outputTokens_;
}

std::string ParserContext::addContextToErrorMessage(const std::string &message) const {
    std::stringstream ss;
    ss  << std::endl << "state stack: " << std::endl;
    if (stateStack_.empty()) {
        ss << "    <empty>" << std::endl;
    }
    for (int i=0; i<stateStack_.size(); i++) {
        auto s = stateStack_.at(i);
        ss << "    " << i << ": " << to_string(s) << std::endl;
    }
    ss << "output tokens: " << std::endl;
    for (int i=0; i<outputTokens_.size(); i++) {
        auto s = outputTokens_.at(i);
        ss << "    " << i << ": " << s.toString() << std::endl;
    }
    if (outputTokens_.empty()) {
        ss << "    <empty>" << std::endl;
    }
    ss << "message: " << message << std::endl;
    ss << "location: " << line_.getFileLocation().toString() << std::endl;
    return ss.str();
}

ParserState ParserContext::getCurrentState() const {
    if (stateStack_.empty()) {
        throw Exception(addContextToErrorMessage("ParserContext::getCurrentState went haywire: State transition messed up"));
    }
    return stateStack_.back();
}

ParserException ParserContext::parserException(const std::string& message)
{
    return ParserException(addContextToErrorMessage(message));
}

ClosingUnopenedBlockException ParserContext::closingUnopenedBlockException(const parser::ParserToken& token)
{
    return ClosingUnopenedBlockException(token);
}

UnknownEscapeCharacterException ParserContext::unknownEscapeCharacterException(const parser::ParserToken& token)
{
    return UnknownEscapeCharacterException(token);
}

InvalidTokenInThisContextException ParserContext::invalidTokenInThisContextException(const parser::ParserToken& token, const states::ParserState state, const std::string &message)
{
    return InvalidTokenInThisContextException(token, state, addContextToErrorMessage(message));
}

UnclosedOpenedBlockException ParserContext::unclosedOpenedBlockException(const std::string &message)
{
    return UnclosedOpenedBlockException(addContextToErrorMessage(message));
}

lexer::LexerException ParserContext::lexerException(const std::string& message)
{
    return lexer::LexerException(addContextToErrorMessage(message));
}

Exception ParserContext::exception(const std::string& message)
{
    return Exception(addContextToErrorMessage(message));
}


} // namespace states
} // namespace parser
} // namespace yapllang
} // namespace org
