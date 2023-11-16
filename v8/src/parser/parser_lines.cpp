#include "parser_lines.hpp"
#include "lexer/tokenizer/tokenizer.hpp"
#include "lexer/tokenizer/tokenizer_lines.hpp"
#include "parser_exception.hpp"
#include "states/parser_context.hpp"
#include "states/parser_states.hpp"
#include "states/handling_indented_block.hpp"
#include "states/handling_normal_stuff.hpp"
#include "states/handling_single_line_comment.hpp"
#include "states/handling_quoted_string.hpp"
#include "states/handling_multi_line_string.hpp"
#include "states/handling_parenthesis.hpp"
#include "states/handling_brackets.hpp"
#include "states/handling_curly_braces.hpp"
#include "states/handle_begin_of_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace parser {

using states::ParserState;
using states::ParserContext;
using tokenizer::TokenizerToken;
using tokenizer::TokenizerTokenType;

ParserLines::ParserLines() {
}

ParserLines::ParserLines(const ParserLines& other)
    : lines_(other.lines_)
{
}

ParserLines& ParserLines::operator=(const ParserLines& other) {
    if (this != &other) {
        lines_ = other.lines_;
    }
    return *this;
}

void ParserLines::addLine(const ParserLine& line) {
    lines_.emplace_back(line);
}

ParserLines::iterator ParserLines::begin() const {
    return lines_.begin();
}

ParserLines::iterator ParserLines::end() const {
    return lines_.end();
}

bool maybeMergeTokens(std::vector<TokenizerToken>::iterator &currentToken) {
    auto previousToken = std::prev(currentToken);
    if (previousToken->type == currentToken->type) {
        if (currentToken->type == TokenizerTokenType::COMMENT_CONTENT
        || currentToken->type == TokenizerTokenType::STRING_CONTENT) {
            auto expectedNextToken = previousToken->location.getFileOffsetInBytes() + previousToken->text.size();
            if (expectedNextToken == currentToken->location.getFileOffsetInBytes()) {
                previousToken->text.append(currentToken->text);
                return true;
            }
        }
    }
    return false;
}

void handleEndOfLine(ParserContext& context) {
    bool loop = true;
    while (loop) {
        loop = false;
        auto state = context.getCurrentState();
        switch (state) {
            case ParserState::STARTING_INDENTED_BLOCK:
            case ParserState::HANDLING_INDENTED_BLOCK:
            case ParserState::HANDLING_BEGIN_FILE:
            case ParserState::HANDLING_NORMAL_STUFF:
            case ParserState::HANDLING_MULTI_LINE_STRING:
            case ParserState::HANDLING_PARENTHESIS:
            case ParserState::HANDLING_BRACKETS:
            case ParserState::HANDLING_CURLY_BRACES:
                break;

            case ParserState::HANDLING_SINGLE_LINE_COMMENT:
                {
                    context.pop(ParserState::HANDLING_SINGLE_LINE_COMMENT);
                    tokenizer::TokenizerToken newToken({
                        TokenizerTokenType::END_SINGLE_LINE_COMMENT,
                        "",
                        context.getCurrentLine().getFileLocation()
                    });
                    context.pushOutputToken(newToken);
                    loop = true;
                }
                break;

            case ParserState::HANDLING_QUOTED_STRING:
                throw context.unclosedOpenedBlockException("missing closing quote");

            default:
                throw context.exception("unexpected state (" + to_string(state) + ") at EOL");
        }
    }
    std::vector<tokenizer::TokenizerToken> &tokens = context.mutateOutputTokens();
    auto it = tokens.begin();
    while (it != tokens.end()) {
        // Check if the current element is equal to the previous one
        if (it != tokens.begin() && maybeMergeTokens(it)) {
            it = tokens.erase(it);
        } else {
            // Move to the next element
            ++it;
        }
    }
}

void handleEndOfFile(ParserContext& context) {
    bool loop = true;
    while (loop) {
        loop = false;
        auto state = context.getCurrentState();
        switch (state) {
            case ParserState::HANDLING_BEGIN_FILE:
                break;

            case ParserState::HANDLING_NORMAL_STUFF:
                break;

            case ParserState::HANDLING_SINGLE_LINE_COMMENT:
                {
                    context.pop(ParserState::HANDLING_SINGLE_LINE_COMMENT);
                    tokenizer::TokenizerToken newToken({
                        TokenizerTokenType::END_SINGLE_LINE_COMMENT,
                        "",
                        context.getCurrentLine().getFileLocation()
                    });
                    context.pushOutputToken(newToken);
                    loop = true;
                }
                break;

            case ParserState::HANDLING_MULTI_LINE_STRING:
                throw context.unclosedOpenedBlockException("missing multi-line string terminator");

            case ParserState::HANDLING_PARENTHESIS:
                throw context.unclosedOpenedBlockException("missing closing parenthesis");

            case ParserState::HANDLING_BRACKETS:
                throw context.unclosedOpenedBlockException("missing closing bracket");

            case ParserState::HANDLING_CURLY_BRACES:
                throw context.unclosedOpenedBlockException("missing closing curly braces");

            case ParserState::HANDLING_QUOTED_STRING:
                throw context.unclosedOpenedBlockException("missing closing quote");

            case ParserState::STARTING_INDENTED_BLOCK:
                throw context.unclosedOpenedBlockException("expected indented block following :");

            case ParserState::HANDLING_INDENTED_BLOCK:
                {
                    int dedents = context.maybeDedent("");
                    while (dedents-- > 0) {
                        context.pop(ParserState::HANDLING_INDENTED_BLOCK);
                        tokenizer::TokenizerToken newToken({
                            TokenizerTokenType::END_BLOCK,
                            "",
                            context.getCurrentLine().getFileLocation()
                        });
                        context.pushOutputToken(newToken);
                    }
                }
                break;

            default:
                throw context.exception("unexpected state (" + to_string(state) + "=" + std::to_string(static_cast<int>(state)) + ") at EOF");
        }
    }
    if (context.getCurrentState() != ParserState::HANDLING_BEGIN_FILE) {
        throw context.parserException("context state not empty at end-of-file");
    }
}

ParserLines ParserLines::parse(const lexer::tokenizer::TokenizerLines& lines) {
    ParserLines lineTokens;
    std::vector<ParserState> stateStack;
    std::vector<size_t> indentation;
    stateStack.push_back(ParserState::HANDLING_BEGIN_FILE);
    for (auto line : lines) {
        ParserContext context(line, stateStack, indentation);
        handleBeginOfLine(context);
        for (auto token : line.getTokens()) {
            auto currentState = context.getCurrentState();
            switch (currentState) {
                case ParserState::HANDLING_BEGIN_FILE:
                case ParserState::HANDLING_NORMAL_STUFF:
                    handlingNormalStuff(token, context);
                    break;
                case ParserState::HANDLING_SINGLE_LINE_COMMENT:
                    handlingSingleLineComment(token, context);
                    break;
                case ParserState::HANDLING_QUOTED_STRING:
                    handlingQuotedString(token, context);
                    break;
                case ParserState::HANDLING_MULTI_LINE_STRING:
                    handlingMultiLineString(token, context);
                    break;
                case ParserState::HANDLING_PARENTHESIS:
                    handlingParenthesis(token, context);
                    break;
                case ParserState::HANDLING_BRACKETS:
                    handlingBrackets(token, context);
                    break;
                case ParserState::HANDLING_CURLY_BRACES:
                    handlingCurlyBraces(token, context);
                    break;
                case ParserState::HANDLING_INDENTED_BLOCK:
                    handlingIndentedBlock(token, context);
                    break;
                default:
                    throw context.exception("unexpected state (" + to_string(currentState) + ") encountered during decontextualization");
            }
        }
        handleEndOfLine(context);
        auto lineToAdd = ParserLine(line, context.getOutputTokens());
        lineTokens.addLine(lineToAdd);
    }
    ParserContext eofContext(lines.getEOFAsTokenizerLine(), stateStack, indentation);
    handleEndOfFile(eofContext);
    if (!eofContext.getOutputTokens().empty())
    {
        auto lineToAdd = ParserLine(eofContext.getCurrentLine(), eofContext.getOutputTokens());
        lineTokens.addLine(lineToAdd);
    }
    return lineTokens;
}

void ParserLines::print() const {

    // TODO: this is copy-pasta with TokenizerLines, deal with it

    // Print the tokens per line
    for (const ParserLine& line : lines_) {
        if (line.empty()) {
            continue;
        }
        std::cout << line.toString();
    }
}

} // namespace parser
} // namespace lexer
} // namespace yapllang
} // namespace org
