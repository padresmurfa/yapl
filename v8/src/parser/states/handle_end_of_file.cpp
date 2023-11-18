#include "handle_end_of_file.hpp"

namespace org {
namespace yapllang {
namespace parser {
namespace states {

using states::ParserState;
using states::ParserContext;
using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;

bool maybeMergeFileTokens(std::vector<ParserToken>::iterator &currentToken) {
    /*
    TODO: multi-line constructs should be merged at this point in time
    */
    return false;
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
                    ParserToken newToken({
                        ParserTokenType::END_SINGLE_LINE_COMMENT,
                        "",
                        context.getCurrentLine().getFileLocation()
                    });
                    context.pushOutputToken(newToken);
                    loop = true;
                }
                break;

            case ParserState::HANDLING_MULTI_LINE_COMMENT:
                throw context.unclosedOpenedBlockException("missing multi-line comment terminator");

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
                        ParserToken newToken({
                            ParserTokenType::END_BLOCK,
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
    std::vector<ParserToken> &tokens = context.mutateOutputTokens();
    auto it = tokens.begin();
    while (it != tokens.end()) {
        // Check if the current element is equal to the previous one
        if (it != tokens.begin() && maybeMergeFileTokens(it)) {
            it = tokens.erase(it);
        } else {
            // Move to the next element
            ++it;
        }
    }
}

} // namespace states
} // namespace parser
} // namespace yapllang
} // namespace org
