#include "handle_end_of_line.hpp"

namespace org {
namespace yapllang {
namespace parser {
namespace states {

using states::ParserState;
using states::ParserContext;
using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;

bool maybeMergeAdjacentContentTokens(std::vector<ParserToken>::iterator &previousToken, const std::vector<ParserToken>::iterator &currentToken) {
    if (previousToken->type == currentToken->type) {
        if (currentToken->type == ParserTokenType::TMP_SINGLE_LINE_COMMENT_CONTENT
        || currentToken->type == ParserTokenType::TMP_MULTI_LINE_COMMENT_CONTENT
        || currentToken->type == ParserTokenType::TMP_STRING_CONTENT) {
            if (maybeMergeToken(*previousToken, *currentToken)) {
                return true;
            }
        }
    }
    return false;
}

bool maybeMergeSingleLineCommentTokens(std::vector<ParserToken>::iterator &previousToken, std::vector<ParserToken>::iterator &currentToken) {
    if (previousToken->type == ParserTokenType::TMP_BEGIN_SINGLE_LINE_COMMENT && currentToken->type == ParserTokenType::TMP_SINGLE_LINE_COMMENT_CONTENT) {
        if (maybeMergeToken(*previousToken, *currentToken)) {
            return true;
        }
    }
    if ((previousToken->type == ParserTokenType::TMP_BEGIN_SINGLE_LINE_COMMENT || 
            previousToken->type == ParserTokenType::TMP_SINGLE_LINE_COMMENT_CONTENT) &&
            currentToken->type == ParserTokenType::TMP_END_SINGLE_LINE_COMMENT
        ) {
        mergeToken(*previousToken, *currentToken);
        previousToken->type = ParserTokenType::TMP_SINGLE_LINE_COMMENT_CONTENT;
        return true;
    }
    return false;
}

bool maybeMergeSingleLineStringTokens(std::vector<ParserToken>::iterator &previousToken, std::vector<ParserToken>::iterator &currentToken) {
    if (previousToken->type == ParserTokenType::TMP_BEGIN_SINGLE_LINE_STRING && currentToken->type == ParserTokenType::TMP_STRING_CONTENT) {
        if (maybeMergeToken(*previousToken, *currentToken)) {
            return true;
        }
    }
    if (previousToken->type == ParserTokenType::TMP_BEGIN_SINGLE_LINE_STRING && currentToken->type == ParserTokenType::TMP_END_SINGLE_LINE_STRING) {
        mergeToken(*previousToken, *currentToken);
        previousToken->type = ParserTokenType::TMP_STRING_CONTENT;
        previousToken->text = previousToken->text.substr(1, previousToken->text.size()-2);
        return true;
    }
    return false;
}

bool maybeMergeLineTokens(std::vector<ParserToken>::iterator &currentToken) {
    auto previousToken = std::prev(currentToken);
    auto tmp = *previousToken;
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

void assertMultiLineCommentDelimiterIsAloneOnLine(ParserContext& context) {
    const std::vector<parser::ParserToken>& outputTokens = context.getOutputTokens();
    int foundDelimiter = 0;
    bool foundSomethingElse = false;
    for (auto it = outputTokens.begin(); it != outputTokens.end(); it++) {
        switch (it->type) {
            case ParserTokenType::BEGIN_BLOCK:
            case ParserTokenType::END_BLOCK:
                // a multi-line comment delimiter may indent/dedent blocks
                break;

            case ParserTokenType::TMP_BEGIN_MULTI_LINE_COMMENT:
            case ParserTokenType::TMP_END_MULTI_LINE_COMMENT:
                foundDelimiter++;
                break;
            default:
                foundSomethingElse = true;
                break;
        }
    }
    if (foundDelimiter > 1) {
        throw context.exception("at most one multi-line comment delimiter token may be present in each line of code");
    }
    if (foundDelimiter > 0 && foundSomethingElse) {
        throw context.exception("multi-line comment delimiters must be alone in a line of code");
    }
}

void assertMultiLineStringDelimiterIsAloneOnLine(ParserContext& context) {
    const std::vector<parser::ParserToken>& outputTokens = context.getOutputTokens();
    int foundDelimiter = 0;
    bool foundSomethingElse = false;
    for (auto it = outputTokens.begin(); it != outputTokens.end(); it++) {
        switch (it->type) {
            case ParserTokenType::BEGIN_BLOCK:
            case ParserTokenType::END_BLOCK:
                // a multi-line comment delimiter may indent/dedent blocks
                break;

            case ParserTokenType::TMP_BEGIN_MULTI_LINE_STRING:
            case ParserTokenType::TMP_END_MULTI_LINE_STRING:
                foundDelimiter++;
                break;
            default:
                foundSomethingElse = true;
                break;
        }
    }
    if (foundDelimiter > 1) {
        throw context.exception("at most one multi-line string delimiter token may be present in each line of code");
    }
    if (foundDelimiter > 0 && foundSomethingElse) {
        throw context.exception("multi-line string delimiters must be alone in a line of code");
    }
}

void handleEndOfLine(ParserContext& context) {
    bool loop = true;
    while (loop) {
        loop = false;
        auto state = context.getCurrentState();
        switch (state) {
            case ParserState::HANDLING_MULTI_LINE_COMMENT:
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
                    auto eol = context.getCurrentLine().getFileArea().asEndOfArea();
                    context.pop(ParserState::HANDLING_SINGLE_LINE_COMMENT);
                    ParserToken newToken({
                        ParserTokenType::TMP_END_SINGLE_LINE_COMMENT,
                        "",
                        eol
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
    assertMultiLineCommentDelimiterIsAloneOnLine(context);
    assertMultiLineStringDelimiterIsAloneOnLine(context);
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
