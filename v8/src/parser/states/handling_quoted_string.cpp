#include "handling_quoted_string.hpp"
#include "unescape_character.hpp"

namespace org {
namespace yapllang {
namespace parser {
namespace states {

using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;


void handlingQuotedString(const TokenizerToken &token, ParserContext& context) {
    switch (token.type) {
        case TokenizerTokenType::QUOTED_STRING:
            {
                context.pop(ParserState::HANDLING_QUOTED_STRING, ParserToken::from(token, ParserTokenType::TMP_END_SINGLE_LINE_STRING));
            }
            break;

        case TokenizerTokenType::ESCAPED_CHARACTER:
            {
                ParserToken newToken(ParserToken::from(token, ParserTokenType::TMP_STRING_CONTENT));
                newToken.text = unescapeCharacter(newToken.text.substr(1), newToken);
                context.pushOutputToken(newToken);
            }
            break;

        case TokenizerTokenType::NORMAL:
        case TokenizerTokenType::COMMA:
        case TokenizerTokenType::MINUS_MINUS:
        case TokenizerTokenType::MINUS_MINUS_MINUS:
        case TokenizerTokenType::MULTI_LINE_STRING:
        case TokenizerTokenType::OPEN_PARENTHESIS:
        case TokenizerTokenType::OPEN_BRACKET:
        case TokenizerTokenType::OPEN_CURLY_BRACE:
        case TokenizerTokenType::COLON:
        case TokenizerTokenType::CLOSE_PARENTHESIS:
        case TokenizerTokenType::CLOSE_CURLY_BRACE:
        case TokenizerTokenType::CLOSE_BRACKET:
            {
                // nothing (except */)) has a special meaning within a multi-line comment in YAPL
                ParserToken newToken(ParserToken::from(token, ParserTokenType::TMP_STRING_CONTENT));
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
