#include "handle_end_of_line.hpp"

namespace org {
namespace yapllang {
namespace parser {
namespace states {

using states::ParserState;
using states::ParserContext;
using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;

void mergeToken(ParserToken& previousToken, const ParserToken& currentToken) {
    // TODO: consider ensuring that the end position of currentToken is available to previousToken, as
    // otherwise its not really possible to ensure that whoever is using our parse tree has totally
    // correct positioning information.
    previousToken.text.append(currentToken.text);
}

bool maybeMergeToken(ParserToken& previousToken, const ParserToken& currentToken) {
    auto expectedNextToken = previousToken.location.getFileOffset() + previousToken.text.size();
    if (expectedNextToken == currentToken.location.getFileOffset()) {
        mergeToken(previousToken, currentToken);
        return true;
    }
    return false;
}

bool maybeMergeAdjacentContentTokens(std::vector<ParserToken>::iterator &previousToken, std::vector<ParserToken>::iterator &currentToken) {
    if (previousToken->type == currentToken->type) {
        if (currentToken->type == ParserTokenType::SINGLE_LINE_COMMENT_CONTENT
        || currentToken->type == ParserTokenType::MULTI_LINE_COMMENT_CONTENT
        || currentToken->type == ParserTokenType::STRING_CONTENT) {
            if (maybeMergeToken(*previousToken, *currentToken)) {
                return true;
            }
        }
    }
    return false;
}

bool maybeMergeSingleLineCommentTokens(std::vector<ParserToken>::iterator &previousToken, std::vector<ParserToken>::iterator &currentToken) {
    if (previousToken->type == ParserTokenType::BEGIN_SINGLE_LINE_COMMENT && currentToken->type == ParserTokenType::SINGLE_LINE_COMMENT_CONTENT) {
        if (maybeMergeToken(*previousToken, *currentToken)) {
            return true;
        }
    }
    if ((previousToken->type == ParserTokenType::BEGIN_SINGLE_LINE_COMMENT || 
            previousToken->type == ParserTokenType::SINGLE_LINE_COMMENT_CONTENT) &&
            currentToken->type == ParserTokenType::END_SINGLE_LINE_COMMENT
        ) {
        mergeToken(*previousToken, *currentToken);
        previousToken->type = ParserTokenType::SINGLE_LINE_COMMENT_CONTENT;
        return true;
    }
    return false;
}

bool maybeMergeSingleLineStringTokens(std::vector<ParserToken>::iterator &previousToken, std::vector<ParserToken>::iterator &currentToken) {
    if (previousToken->type == ParserTokenType::BEGIN_SINGLE_LINE_STRING && currentToken->type == ParserTokenType::STRING_CONTENT) {
        if (maybeMergeToken(*previousToken, *currentToken)) {
            return true;
        }
    }
    if (previousToken->type == ParserTokenType::BEGIN_SINGLE_LINE_STRING && currentToken->type == ParserTokenType::END_SINGLE_LINE_STRING) {
        mergeToken(*previousToken, *currentToken);
        previousToken->type = ParserTokenType::STRING_CONTENT;
        return true;
    }
    return false;
}

bool maybeMergeLineTokens(std::vector<ParserToken>::iterator &currentToken) {
    auto previousToken = std::prev(currentToken);
    if (maybeMergeAdjacentContentTokens(previousToken, currentToken)) {
        return true;
    }
    if (maybeMergeSingleLineCommentTokens(previousToken, currentToken)) {
        return true;
    }
    if (maybeMergeSingleLineStringTokens(previousToken, currentToken)) {
        return true;
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
            case ParserState::HANDLING_MULTI_LINE_COMMENT:
            case ParserState::HANDLING_PARENTHESIS:
            case ParserState::HANDLING_BRACKETS:
            case ParserState::HANDLING_CURLY_BRACES:
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

            case ParserState::HANDLING_QUOTED_STRING:
                throw context.unclosedOpenedBlockException("missing closing quote");

            default:
                throw context.exception("unexpected state (" + to_string(state) + ") at EOL");
        }
    }
    std::vector<ParserToken> &tokens = context.mutateOutputTokens();
    auto it = tokens.begin();
    while (it != tokens.end()) {
        // Check if the current element is equal to the previous one
        if (it != tokens.begin() && maybeMergeLineTokens(it)) {
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
