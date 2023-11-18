#include "handle_begin_of_line.hpp"

namespace org {
namespace yapllang {
namespace parser {
namespace states {

using states::ParserState;
using states::ParserContext;
using lexer::tokenizer::TokenizerLine;
using parser::ParserToken;
using parser::ParserTokenType;

void handleBeginOfLine_StartingIndentedBlock(ParserContext& context, const TokenizerLine& line) {
    if (line.getLineWithoutWhitespace().empty()) {
        // empty lines don't count for indentation/dedentation
        return;
    }
    context.indent(line.getLeadingWhitespace());
    context.pop(ParserState::STARTING_INDENTED_BLOCK);
    parser::ParserToken newToken({
        ParserTokenType::BEGIN_BLOCK,
        "",
        context.getCurrentLine().getFileLocation()
    });
    context.push(ParserState::HANDLING_INDENTED_BLOCK, newToken);
}

void handleBeginOfLine_BeginFileOrNormalStuff(ParserContext& context, const TokenizerLine& line, const ParserState& state) {
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
        context.pop(ParserState::HANDLING_INDENTED_BLOCK);
        parser::ParserToken newToken({
            ParserTokenType::END_BLOCK,
            "",
            context.getCurrentLine().getFileLocation()
        });
        context.pushOutputToken(newToken);
    }
}


void handleBeginOfLine(ParserContext& context) {
    bool loop = true;
    while (loop) {
        loop = false;
        auto line = context.getCurrentLine();
        auto state = context.getCurrentState();
        auto location = line.getFileLocation();
        switch (state) {
            case ParserState::STARTING_INDENTED_BLOCK:
                handleBeginOfLine_StartingIndentedBlock(context, line);
                break;

            case ParserState::HANDLING_SINGLE_LINE_COMMENT:
            case ParserState::HANDLING_QUOTED_STRING:
                throw context.exception("should not begin a line in single-line-comment, semantic-comment, or quoted-string mode");

            case ParserState::HANDLING_PARENTHESIS:
            case ParserState::HANDLING_BRACKETS:
            case ParserState::HANDLING_CURLY_BRACES:
                // note that we don't care about indenting in these states
                if (line.getLineWithoutWhitespace().empty()) {
                    // empty lines don't count for indentation/dedentation
                    break;
                }
                if (context.wouldDedent(line.getLeadingWhitespace())) {
                    throw context.exception("should not dedent within parenthesis, brackets, or curly-braces");
                }
                break;

            case ParserState::HANDLING_BEGIN_FILE:
            case ParserState::HANDLING_NORMAL_STUFF:
            case ParserState::HANDLING_INDENTED_BLOCK:
                handleBeginOfLine_BeginFileOrNormalStuff(context, line, state);
                break;

            case ParserState::HANDLING_MULTI_LINE_COMMENT:
            case ParserState::HANDLING_MULTI_LINE_STRING:
                // we care neither about indenting or dedenting in comments and strings
                // TODO: consider if this is really the case... we probably want to trim leading whitespace from
                //       multi-line strings and comments
                break;

            default:
                throw context.exception("unexpected state (" + to_string(state) + ") at BEGIN-OF-LINE");
        }
    }
}

} // namespace states
} // namespace parser
} // namespace yapllang
} // namespace org
