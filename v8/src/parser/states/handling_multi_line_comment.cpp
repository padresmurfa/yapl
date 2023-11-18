#include "handling_multi_line_comment.hpp"
#include "unescape_character.hpp"

namespace org {
namespace yapllang {
namespace parser {
namespace states {

using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;

void handlingMultiLineComment(const TokenizerToken &token, ParserContext& context) {
    switch (token.type) {
        case TokenizerTokenType::MINUS_MINUS_MINUS:
            {
                ParserToken newToken(ParserToken::from(token, ParserTokenType::END_MULTI_LINE_COMMENT));
                newToken.text = "";
                context.pop(ParserState::HANDLING_MULTI_LINE_COMMENT, newToken);
            }
            break;

        case TokenizerTokenType::ESCAPED_CHARACTER:
        case TokenizerTokenType::NORMAL:
        case TokenizerTokenType::COMMA:
        case TokenizerTokenType::MULTI_LINE_STRING:
        case TokenizerTokenType::MINUS_MINUS:
        case TokenizerTokenType::QUOTED_STRING:
        case TokenizerTokenType::OPEN_PARENTHESIS:
        case TokenizerTokenType::OPEN_BRACKET:
        case TokenizerTokenType::OPEN_CURLY_BRACE:
        case TokenizerTokenType::COLON:
        case TokenizerTokenType::CLOSE_PARENTHESIS:
        case TokenizerTokenType::CLOSE_CURLY_BRACE:
        case TokenizerTokenType::CLOSE_BRACKET:
            {
                // nothing (except */)) has a special meaning within a multi-line comment in YAPL
                ParserToken newToken(ParserToken::from(token, ParserTokenType::MULTI_LINE_COMMENT_CONTENT));
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
