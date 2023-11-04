#include "decontextualizer_context.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {
namespace states {

DecontextualizerContext::DecontextualizerContext(const preprocessor::PreprocessorLine& line, std::vector<DecontextualizerState>& stateStack, std::vector<size_t> &indentation)
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

size_t DecontextualizerContext::getIndentLength() const
{
    size_t result = 0;
    for (auto i : indentation_) {
        result += i;
    }
    return result;
}

void DecontextualizerContext::indent(const std::string &newWhitespace)
{
    auto newWhitespaceLength = lengthOfWhitespace(newWhitespace);
    auto currentWhitespaceLength = getIndentLength();
    if (newWhitespaceLength <= currentWhitespaceLength) {
        throw exception("indenting to (" + std::to_string(newWhitespaceLength) + "), which is our prior indentation level (" + std::to_string(currentWhitespaceLength) + "), or less");
    }
    indentation_.push_back(newWhitespaceLength - currentWhitespaceLength);
}

int DecontextualizerContext::maybeDedent(const std::string &newWhitespace)
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

bool DecontextualizerContext::wouldDedent(const std::string &newWhitespace) const {
    auto newWhitespaceLength = lengthOfWhitespace(newWhitespace);
    auto currentWhitespaceLength = getIndentLength();
    return currentWhitespaceLength > newWhitespaceLength;
}

bool DecontextualizerContext::wouldIndent(const std::string &newWhitespace) const {
    auto newWhitespaceLength = lengthOfWhitespace(newWhitespace);
    auto currentWhitespaceLength = getIndentLength();
    return newWhitespaceLength > currentWhitespaceLength;
}

const preprocessor::PreprocessorLine &DecontextualizerContext::getCurrentLine() const
{
    return line_;
}

void DecontextualizerContext::pushOutputToken(const preprocessor::PreprocessorToken &token) {
    outputTokens_.push_back(token);
}

void DecontextualizerContext::push(DecontextualizerState state, const preprocessor::PreprocessorToken &token) {
    pushOutputToken(token);
    stateStack_.push_back(state);
}

void DecontextualizerContext::pop(DecontextualizerState state, const preprocessor::PreprocessorToken &token) {
    pushOutputToken(token);
    pop(state);
}

bool DecontextualizerContext::emptyState() const {
    return stateStack_.empty();
}

void DecontextualizerContext::pop(DecontextualizerState expectedState) {
    if (stateStack_.empty()) {
        throw Exception(addContextToErrorMessage("DecontextualizerContext::pop went haywire: state-stack was empty"));
    }
    auto currentState = stateStack_.back();
    if (currentState != expectedState) {
        throw Exception(addContextToErrorMessage("DecontextualizerContext::pop went haywire: expected state-stack.top=" + to_string(expectedState) + ", but current state-stack.top=" + to_string(currentState)));
    }
    stateStack_.pop_back();
}

std::vector<preprocessor::PreprocessorToken> &DecontextualizerContext::mutateOutputTokens() {
    return outputTokens_;
}

const std::vector<preprocessor::PreprocessorToken> &DecontextualizerContext::getOutputTokens() {
    return outputTokens_;
}

std::string DecontextualizerContext::addContextToErrorMessage(const std::string &message) const {
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

DecontextualizerState DecontextualizerContext::getCurrentState() const {
    if (stateStack_.empty()) {
        throw Exception(addContextToErrorMessage("DecontextualizerContext::getCurrentState went haywire: State transition messed up"));
    }
    return stateStack_.back();
}

DecontextualizerException DecontextualizerContext::decontextualizerException(const std::string& message)
{
    return DecontextualizerException(addContextToErrorMessage(message));
}

ClosingUnopenedBlockException DecontextualizerContext::closingUnopenedBlockException(const preprocessor::PreprocessorToken& token)
{
    return ClosingUnopenedBlockException(token);
}

UnknownEscapeCharacterException DecontextualizerContext::unknownEscapeCharacterException(const preprocessor::PreprocessorToken& token)
{
    return UnknownEscapeCharacterException(token);
}

InvalidTokenInThisContextException DecontextualizerContext::invalidTokenInThisContextException(const preprocessor::PreprocessorToken& token, const states::DecontextualizerState state, const std::string &message)
{
    return InvalidTokenInThisContextException(token, state, addContextToErrorMessage(message));
}

UnclosedOpenedBlockException DecontextualizerContext::unclosedOpenedBlockException(const std::string &message)
{
    return UnclosedOpenedBlockException(addContextToErrorMessage(message));
}

LexerException DecontextualizerContext::lexerException(const std::string& message)
{
    return LexerException(addContextToErrorMessage(message));
}

Exception DecontextualizerContext::exception(const std::string& message)
{
    return Exception(addContextToErrorMessage(message));
}


} // namespace states
} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org
