#include "decontextualizer_lines.hpp"
#include "lexer/preprocessor/preprocessor.hpp"
#include "lexer/preprocessor/preprocessor_lines.hpp"
#include "decontextualizer_exception.hpp"
#include "states/decontextualizer_context.hpp"
#include "states/decontextualizer_states.hpp"
#include "states/handling_indented_block.hpp"
#include "states/handling_normal_stuff.hpp"
#include "states/handling_single_line_comment.hpp"
#include "states/handling_semantic_comment.hpp"
#include "states/handling_multi_line_comment.hpp"
#include "states/handling_quoted_string.hpp"
#include "states/handling_multi_line_string.hpp"
#include "states/handling_parenthesis.hpp"
#include "states/handling_brackets.hpp"
#include "states/handling_curly_braces.hpp"
#include "states/handle_begin_of_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {

using states::DecontextualizerState;
using states::DecontextualizerContext;
using preprocessor::PreprocessorToken;
using preprocessor::PreprocessorTokenType;

DecontextualizerLines::DecontextualizerLines() {
}

DecontextualizerLines::DecontextualizerLines(const DecontextualizerLines& other)
    : lines_(other.lines_)
{
}

DecontextualizerLines& DecontextualizerLines::operator=(const DecontextualizerLines& other) {
    if (this != &other) {
        lines_ = other.lines_;
    }
    return *this;
}

void DecontextualizerLines::addLine(const DecontextualizerLine& line) {
    lines_.emplace_back(line);
}

DecontextualizerLines::iterator DecontextualizerLines::begin() const {
    return lines_.begin();
}

DecontextualizerLines::iterator DecontextualizerLines::end() const {
    return lines_.end();
}

void handleEndOfLine(DecontextualizerContext& context) {
    bool loop = true;
    while (loop) {
        loop = false;
        auto state = context.getCurrentState();
        switch (state) {
            case DecontextualizerState::STARTING_INDENTED_BLOCK:
            case DecontextualizerState::HANDLING_INDENTED_BLOCK:
            case DecontextualizerState::HANDLING_BEGIN_FILE:
            case DecontextualizerState::HANDLING_NORMAL_STUFF:
            case DecontextualizerState::HANDLING_MULTI_LINE_COMMENT:
            case DecontextualizerState::HANDLING_MULTI_LINE_STRING:
            case DecontextualizerState::HANDLING_PARENTHESIS:
            case DecontextualizerState::HANDLING_BRACKETS:
            case DecontextualizerState::HANDLING_CURLY_BRACES:
                break;

            case DecontextualizerState::HANDLING_SINGLE_LINE_COMMENT:
                context.pop(DecontextualizerState::HANDLING_SINGLE_LINE_COMMENT);
                loop = true;
                break;

            case DecontextualizerState::HANDLING_SEMANTIC_COMMENT:
                context.pop(DecontextualizerState::HANDLING_SEMANTIC_COMMENT);
                loop = true;
                break;

            case DecontextualizerState::HANDLING_QUOTED_STRING:
                throw context.unclosedOpenedBlockException("missing closing quote");

            default:
                throw context.exception("unexpected state (" + to_string(state) + ") at EOL");
        }
    }
}

void handleEndOfFile(DecontextualizerContext& context) {
    bool loop = true;
    while (loop) {
        loop = false;
        auto state = context.getCurrentState();
        switch (state) {
            case DecontextualizerState::HANDLING_BEGIN_FILE:
                break;

            case DecontextualizerState::HANDLING_NORMAL_STUFF:
                break;

            case DecontextualizerState::HANDLING_SINGLE_LINE_COMMENT:
                context.pop(DecontextualizerState::HANDLING_SINGLE_LINE_COMMENT);
                loop = true;
                break;

            case DecontextualizerState::HANDLING_SEMANTIC_COMMENT:
                context.pop(DecontextualizerState::HANDLING_SEMANTIC_COMMENT);
                loop = true;
                break;

            case DecontextualizerState::HANDLING_MULTI_LINE_COMMENT:
                throw context.unclosedOpenedBlockException("missing multi-line comment terminator");

            case DecontextualizerState::HANDLING_MULTI_LINE_STRING:
                throw context.unclosedOpenedBlockException("missing multi-line string terminator");

            case DecontextualizerState::HANDLING_PARENTHESIS:
                throw context.unclosedOpenedBlockException("missing closing parenthesis");

            case DecontextualizerState::HANDLING_BRACKETS:
                throw context.unclosedOpenedBlockException("missing closing bracket");

            case DecontextualizerState::HANDLING_CURLY_BRACES:
                throw context.unclosedOpenedBlockException("missing closing curly braces");

            case DecontextualizerState::HANDLING_QUOTED_STRING:
                throw context.unclosedOpenedBlockException("missing closing quote");

            case DecontextualizerState::STARTING_INDENTED_BLOCK:
                throw context.unclosedOpenedBlockException("expected indented block following :");

            case DecontextualizerState::HANDLING_INDENTED_BLOCK:
                {
                    int dedents = context.maybeDedent("");
                    while (dedents-- > 0) {
                        context.pop(DecontextualizerState::HANDLING_INDENTED_BLOCK);
                        preprocessor::PreprocessorToken newToken({
                            PreprocessorTokenType::END_BLOCK,
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
    if (context.getCurrentState() != DecontextualizerState::HANDLING_BEGIN_FILE) {
        throw context.decontextualizerException("context state not empty at end-of-file");
    }
}

DecontextualizerLines DecontextualizerLines::decontextualize(const lexer::preprocessor::PreprocessorLines& lines) {
    DecontextualizerLines lineTokens;
    std::vector<DecontextualizerState> stateStack;
    std::vector<size_t> indentation;
    stateStack.push_back(DecontextualizerState::HANDLING_BEGIN_FILE);
    for (auto line : lines) {
        DecontextualizerContext context(line, stateStack, indentation);
        handleBeginOfLine(context);
        for (auto token : line.getTokens()) {
            auto currentState = context.getCurrentState();
            switch (currentState) {
                case DecontextualizerState::HANDLING_BEGIN_FILE:
                case DecontextualizerState::HANDLING_NORMAL_STUFF:
                    handlingNormalStuff(token, context);
                    break;
                case DecontextualizerState::HANDLING_SINGLE_LINE_COMMENT:
                    handlingSingleLineComment(token, context);
                    break;
                case DecontextualizerState::HANDLING_SEMANTIC_COMMENT:
                    handlingSemanticComment(token, context);
                    break;
                case DecontextualizerState::HANDLING_MULTI_LINE_COMMENT:
                    handlingMultiLineComment(token, context);
                    break;
                case DecontextualizerState::HANDLING_QUOTED_STRING:
                    handlingQuotedString(token, context);
                    break;
                case DecontextualizerState::HANDLING_MULTI_LINE_STRING:
                    handlingMultiLineString(token, context);
                    break;
                case DecontextualizerState::HANDLING_PARENTHESIS:
                    handlingParenthesis(token, context);
                    break;
                case DecontextualizerState::HANDLING_BRACKETS:
                    handlingBrackets(token, context);
                    break;
                case DecontextualizerState::HANDLING_CURLY_BRACES:
                    handlingCurlyBraces(token, context);
                    break;
                case DecontextualizerState::HANDLING_INDENTED_BLOCK:
                    handlingIndentedBlock(token, context);
                    break;
                default:
                    throw context.exception("unexpected state (" + to_string(currentState) + ") encountered during decontextualization");
            }
        }
        handleEndOfLine(context);
        auto lineToAdd = DecontextualizerLine(line, context.getOutputTokens());
        lineTokens.addLine(lineToAdd);
    }
    DecontextualizerContext eofContext(lines.getEOFAsPreprocessorLine(), stateStack, indentation);
    handleEndOfFile(eofContext);
    if (!eofContext.getOutputTokens().empty())
    {
        auto lineToAdd = DecontextualizerLine(eofContext.getCurrentLine(), eofContext.getOutputTokens());
        lineTokens.addLine(lineToAdd);
    }
    return lineTokens;
}

void DecontextualizerLines::print() const {

    // TODO: this is copy-pasta with PreprocessorLines, deal with it

    // Print the tokens per line
    for (const DecontextualizerLine& line : lines_) {
        if (line.empty()) {
            continue;
        }
        std::cout << line.toString();
    }
}

} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org
