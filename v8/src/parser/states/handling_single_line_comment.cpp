#include "handling_single_line_comment.hpp"
 
namespace org {
namespace yapllang {
namespace lexer {
namespace parser {
namespace states {

void handlingSingleLineComment(const tokenizer::TokenizerToken &token, ParserContext& context) {
    switch (token.type) {
        case tokenizer::TokenizerTokenType::NORMAL:
        case tokenizer::TokenizerTokenType::COMMA:
        case tokenizer::TokenizerTokenType::MINUS_MINUS:
        case tokenizer::TokenizerTokenType::MINUS_MINUS_MINUS:
        case tokenizer::TokenizerTokenType::QUOTED_STRING:
        case tokenizer::TokenizerTokenType::ESCAPED_CHARACTER:
        case tokenizer::TokenizerTokenType::MULTI_LINE_STRING:
        case tokenizer::TokenizerTokenType::OPEN_PARENTHESIS:
        case tokenizer::TokenizerTokenType::OPEN_BRACKET:
        case tokenizer::TokenizerTokenType::OPEN_CURLY_BRACE:
        case tokenizer::TokenizerTokenType::COLON:
        case tokenizer::TokenizerTokenType::CLOSE_PARENTHESIS:
        case tokenizer::TokenizerTokenType::CLOSE_CURLY_BRACE:
        case tokenizer::TokenizerTokenType::CLOSE_BRACKET:
            {
                // nothing has a special meaning within a single-line comment in YAPL
                tokenizer::TokenizerToken newToken(token);
                newToken.type = tokenizer::TokenizerTokenType::COMMENT_CONTENT;
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
