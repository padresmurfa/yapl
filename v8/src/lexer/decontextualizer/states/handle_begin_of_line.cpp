#include "handle_begin_of_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {
namespace states {

using states::DecontextualizerState;
using states::DecontextualizerContext;
using preprocessor::PreprocessorLine;
using preprocessor::PreprocessorToken;
using preprocessor::PreprocessorTokenType;

void handleBeginOfLine_StartingIndentedBlock(DecontextualizerContext& context, const PreprocessorLine& line) {
    if (line.getLineWithoutWhitespace().empty()) {
        // empty lines don't count for indentation/dedentation
        return;
    }
    context.indent(line.getLeadingWhitespace());
    context.pop(DecontextualizerState::STARTING_INDENTED_BLOCK);
    preprocessor::PreprocessorToken newToken({
        PreprocessorTokenType::BEGIN_BLOCK,
        "",
        context.getCurrentLine().getFileLocation()
    });
    context.push(DecontextualizerState::HANDLING_INDENTED_BLOCK, newToken);
}

void handleBeginOfLine_BeginFileOrNormalStuff(DecontextualizerContext& context, const PreprocessorLine& line, const DecontextualizerState& state) {
    if (line.getLineWithoutWhitespace().empty()) {
        // empty lines don't count for indentation/dedentation
        return;
    }
    auto leadingWhitespace = line.getLeadingWhitespace();
    if (context.wouldIndent(leadingWhitespace)) {
        throw context.exception(
            "should not indent at beginning of file or during normal code processing (state=" + to_string(state)
            + ", newLeadingWhitespaceLength=" + std::to_string(leadingWhitespace.size())
            + ", currentLeadingWhitespaceLength=" + std::to_string(context.getIndentLength())
            + ")"
        );
    }
    int dedents = context.maybeDedent(line.getLeadingWhitespace());
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


void handleBeginOfLine(DecontextualizerContext& context) {
    bool loop = true;
    while (loop) {
        loop = false;
        auto line = context.getCurrentLine();
        auto state = context.getCurrentState();
        auto location = line.getFileLocation();
        switch (state) {
            case DecontextualizerState::STARTING_INDENTED_BLOCK:
                handleBeginOfLine_StartingIndentedBlock(context, line);
                break;

            case DecontextualizerState::HANDLING_SINGLE_LINE_COMMENT:
            case DecontextualizerState::HANDLING_QUOTED_STRING:
                throw context.exception("should not begin a line in single-line-comment, semantic-comment, or quoted-string mode");

            case DecontextualizerState::HANDLING_PARENTHESIS:
            case DecontextualizerState::HANDLING_BRACKETS:
            case DecontextualizerState::HANDLING_CURLY_BRACES:
                // note that we don't care about indenting in these states
                if (line.getLineWithoutWhitespace().empty()) {
                    // empty lines don't count for indentation/dedentation
                    break;
                }
                if (context.wouldDedent(line.getLeadingWhitespace())) {
                    throw context.exception("should not dedent within parenthesis, brackets, or curly-braces");
                }
                break;

            case DecontextualizerState::HANDLING_BEGIN_FILE:
            case DecontextualizerState::HANDLING_NORMAL_STUFF:
            case DecontextualizerState::HANDLING_INDENTED_BLOCK:
                handleBeginOfLine_BeginFileOrNormalStuff(context, line, state);
                break;

            case DecontextualizerState::HANDLING_MULTI_LINE_STRING:
                // we care neither about indenting or dedenting in comments and strings
                // TODO: consider if this is really the case...
                break;

            default:
                throw context.exception("unexpected state (" + to_string(state) + ") at BEGIN-OF-LINE");
        }
    }
}

} // namespace states
} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org
