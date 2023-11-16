#include "handling_multi_line_string.hpp"
#include "unescape_character.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace parser {
namespace states {

void handlingMultiLineString(const tokenizer::TokenizerToken &token, ParserContext& context) {
    switch (token.type) {
        case tokenizer::TokenizerTokenType::MULTI_LINE_STRING:
            {
                tokenizer::TokenizerToken newToken(token);
                newToken.type = tokenizer::TokenizerTokenType::END_SINGLE_LINE_STRING;
                context.push(ParserState::HANDLING_QUOTED_STRING, newToken);
            }
            break;

        case tokenizer::TokenizerTokenType::ESCAPED_CHARACTER:
            {
                tokenizer::TokenizerToken newToken(token);
                newToken.type = tokenizer::TokenizerTokenType::STRING_CONTENT;
                newToken.text = unescapeCharacter(newToken.text.substr(1), newToken);
                context.pushOutputToken(newToken);
            }
            break;

        case tokenizer::TokenizerTokenType::NORMAL:
        case tokenizer::TokenizerTokenType::COMMA:
        case tokenizer::TokenizerTokenType::MINUS_MINUS_MINUS:
        case tokenizer::TokenizerTokenType::MINUS_MINUS:
        case tokenizer::TokenizerTokenType::QUOTED_STRING:
        case tokenizer::TokenizerTokenType::OPEN_PARENTHESIS:
        case tokenizer::TokenizerTokenType::OPEN_BRACKET:
        case tokenizer::TokenizerTokenType::OPEN_CURLY_BRACE:
        case tokenizer::TokenizerTokenType::COLON:
        case tokenizer::TokenizerTokenType::CLOSE_PARENTHESIS:
        case tokenizer::TokenizerTokenType::CLOSE_CURLY_BRACE:
        case tokenizer::TokenizerTokenType::CLOSE_BRACKET:
            {
                // nothing (except */)) has a special meaning within a multi-line comment in YAPL
                tokenizer::TokenizerToken newToken(token);
                newToken.type = tokenizer::TokenizerTokenType::STRING_CONTENT;
                context.pushOutputToken(newToken);
            }
            break;

        default:
            throw context.exception("unexpected tokenizer token type encounted");
    };
}

} // namespace states
} // namespace parser
} // namespace lexer
} // namespace yapllang
} // namespace org
