#include "handling_curly_braces.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace parser {
namespace states {

void handlingCurlyBraces(const tokenizer::TokenizerToken &token, ParserContext& context) {
    switch (token.type) {
        case tokenizer::TokenizerTokenType::CLOSE_CURLY_BRACE:
            {
                context.pop(ParserState::HANDLING_CURLY_BRACES, token);
            }
            break;

        case tokenizer::TokenizerTokenType::ESCAPED_CHARACTER:
            throw context.invalidTokenInThisContextException(token, ParserState::HANDLING_CURLY_BRACES, "An escaped character is not expected as a token within a curly-braces-block");

        case tokenizer::TokenizerTokenType::COLON:
            // TODO: maps have forms like { a: b }
            throw context.invalidTokenInThisContextException(token, ParserState::HANDLING_CURLY_BRACES, "A colon is not expected as a token within a curly-braces-block");

        case tokenizer::TokenizerTokenType::CLOSE_BRACKET:
            throw context.closingUnopenedBlockException(token);

        case tokenizer::TokenizerTokenType::CLOSE_PARENTHESIS:
            throw context.closingUnopenedBlockException(token);

        case tokenizer::TokenizerTokenType::MINUS_MINUS_MINUS:
            throw context.invalidTokenInThisContextException(token, ParserState::HANDLING_CURLY_BRACES, "A comment-line-separator token is not expected as a token within a curly-braces-block");

        case tokenizer::TokenizerTokenType::MINUS_MINUS:
            {
                tokenizer::TokenizerToken newToken(token);
                newToken.type = tokenizer::TokenizerTokenType::BEGIN_SINGLE_LINE_COMMENT;
                context.push(ParserState::HANDLING_SINGLE_LINE_COMMENT, newToken);
            }
            break;

        case tokenizer::TokenizerTokenType::QUOTED_STRING:
            {
                tokenizer::TokenizerToken newToken(token);
                newToken.type = tokenizer::TokenizerTokenType::BEGIN_SINGLE_LINE_STRING;
                context.push(ParserState::HANDLING_QUOTED_STRING, newToken);
            }
            break;

        case tokenizer::TokenizerTokenType::MULTI_LINE_STRING:
            {
                tokenizer::TokenizerToken newToken(token);
                newToken.type = tokenizer::TokenizerTokenType::BEGIN_MULTI_LINE_STRING;
                context.push(ParserState::HANDLING_MULTI_LINE_STRING, newToken);
            }
            break;

        case tokenizer::TokenizerTokenType::OPEN_PARENTHESIS:
            context.push(ParserState::HANDLING_CURLY_BRACES, token);
            break;

        case tokenizer::TokenizerTokenType::OPEN_BRACKET:
            context.push(ParserState::HANDLING_CURLY_BRACES, token);
            break;

        case tokenizer::TokenizerTokenType::OPEN_CURLY_BRACE:
            context.push(ParserState::HANDLING_CURLY_BRACES, token);
            break;

        case tokenizer::TokenizerTokenType::NORMAL:
        case tokenizer::TokenizerTokenType::COMMA:
            context.pushOutputToken(token);
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
