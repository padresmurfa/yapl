#include "handling_single_line_comment.hpp"
 
namespace org {
namespace yapllang {
namespace parser {
namespace states {

using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;

void handlingSingleLineComment(const TokenizerToken &token, ParserContext& context) {
    switch (token.type) {
        case TokenizerTokenType::NORMAL:
        case TokenizerTokenType::COMMA:
        case TokenizerTokenType::MINUS_MINUS:
        case TokenizerTokenType::MINUS_MINUS_MINUS:
        case TokenizerTokenType::QUOTED_STRING:
        case TokenizerTokenType::ESCAPED_CHARACTER:
        case TokenizerTokenType::MULTI_LINE_STRING:
        case TokenizerTokenType::OPEN_PARENTHESIS:
        case TokenizerTokenType::OPEN_BRACKET:
        case TokenizerTokenType::OPEN_CURLY_BRACE:
        case TokenizerTokenType::COLON:
        case TokenizerTokenType::CLOSE_PARENTHESIS:
        case TokenizerTokenType::CLOSE_CURLY_BRACE:
        case TokenizerTokenType::CLOSE_BRACKET:
            {
                // nothing has a special meaning within a single-line comment in YAPL
                ParserToken newToken(ParserToken::from(token, ParserTokenType::TEMPORARY_SINGLE_LINE_COMMENT_CONTENT));
                context.pushOutputToken(newToken);
            }
            break;

        default:
            throw context.exception("unexpected tokenizer token type encounted");
    };
}

} // namespace states
} // namespace parser
} // namespace yapllang
} // namespace org
