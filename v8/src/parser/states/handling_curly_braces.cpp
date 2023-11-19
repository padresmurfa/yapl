#include "handling_curly_braces.hpp"

namespace org {
namespace yapllang {
namespace parser {
namespace states {

using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;

void handlingCurlyBraces(const TokenizerToken &token, ParserContext& context) {
    switch (token.type) {
        case TokenizerTokenType::CLOSE_CURLY_BRACE:
            {
                context.pop(ParserState::HANDLING_CURLY_BRACES, ParserToken::from(token));
            }
            break;

        case TokenizerTokenType::ESCAPED_CHARACTER:
            throw context.invalidTokenInThisContextException(ParserToken::from(token), ParserState::HANDLING_CURLY_BRACES, "An escaped character is not expected as a token within a curly-braces-block");

        case TokenizerTokenType::COLON:
            // TODO: maps have forms like { a: b }
            throw context.invalidTokenInThisContextException(ParserToken::from(token), ParserState::HANDLING_CURLY_BRACES, "A colon is not expected as a token within a curly-braces-block");

        case TokenizerTokenType::CLOSE_BRACKET:
            throw context.closingUnopenedBlockException(ParserToken::from(token));

        case TokenizerTokenType::CLOSE_PARENTHESIS:
            throw context.closingUnopenedBlockException(ParserToken::from(token));

        case TokenizerTokenType::MINUS_MINUS_MINUS:
            {
                ParserToken newToken(ParserToken::from(token, ParserTokenType::TMP_BEGIN_MULTI_LINE_COMMENT));
                newToken.text = "";
                context.push(ParserState::HANDLING_MULTI_LINE_COMMENT, newToken);
            }
            break;

        case TokenizerTokenType::MINUS_MINUS:
            {
                ParserToken newToken(ParserToken::from(token, ParserTokenType::TMP_BEGIN_SINGLE_LINE_COMMENT));
                context.push(ParserState::HANDLING_SINGLE_LINE_COMMENT, newToken);
            }
            break;

        case TokenizerTokenType::QUOTED_STRING:
            {
                ParserToken newToken(ParserToken::from(token, ParserTokenType::BEGIN_SINGLE_LINE_STRING));
                context.push(ParserState::HANDLING_QUOTED_STRING, newToken);
            }
            break;

        case TokenizerTokenType::MULTI_LINE_STRING:
            {
                ParserToken newToken(ParserToken::from(token, ParserTokenType::BEGIN_MULTI_LINE_STRING));
                context.push(ParserState::HANDLING_MULTI_LINE_STRING, newToken);
            }
            break;

        case TokenizerTokenType::OPEN_PARENTHESIS:
            context.push(ParserState::HANDLING_CURLY_BRACES, ParserToken::from(token));
            break;

        case TokenizerTokenType::OPEN_BRACKET:
            context.push(ParserState::HANDLING_CURLY_BRACES, ParserToken::from(token));
            break;

        case TokenizerTokenType::OPEN_CURLY_BRACE:
            context.push(ParserState::HANDLING_CURLY_BRACES, ParserToken::from(token));
            break;

        case TokenizerTokenType::NORMAL:
        case TokenizerTokenType::COMMA:
            context.pushOutputToken(ParserToken::from(token));
            break;

        default:
            throw context.exception("unexpected tokenizer token type encounted");
    };
}

} // namespace states
} // namespace parser
} // namespace yapllang
} // namespace org
