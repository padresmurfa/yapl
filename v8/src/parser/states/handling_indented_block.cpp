#include "handling_indented_block.hpp"

namespace org {
namespace yapllang {
namespace parser {
namespace states {

using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;

void handlingIndentedBlock(const TokenizerToken &token, ParserContext& context) {
    // TODO: identical to normal stuff, fix the duplication
    switch (token.type) {
       case TokenizerTokenType::NORMAL:
            context.pushOutputToken(ParserToken::from(token));
            break;

        case TokenizerTokenType::COMMA:
            {
                // Commas have no special meaning within a normal/default section of YAPL
                ParserToken newToken(ParserToken::from(token, ParserTokenType::NORMAL));
                context.pushOutputToken(newToken);
            }
            break;

        case TokenizerTokenType::ESCAPED_CHARACTER:
            throw context.invalidTokenInThisContextException(ParserToken::from(token), ParserState::HANDLING_NORMAL_STUFF, "An escaped-character token is not expected as a token within a normal-block");

        case TokenizerTokenType::MINUS_MINUS_MINUS:
            {
                ParserToken newToken(ParserToken::from(token, ParserTokenType::BEGIN_MULTI_LINE_COMMENT));
                newToken.text = "";
                context.push(ParserState::HANDLING_MULTI_LINE_COMMENT, newToken);
            }
            break;

        case TokenizerTokenType::MINUS_MINUS:
            {
                ParserToken newToken(ParserToken::from(token, ParserTokenType::BEGIN_SINGLE_LINE_COMMENT));
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
            context.push(ParserState::HANDLING_PARENTHESIS, ParserToken::from(token));
            break;
        case TokenizerTokenType::OPEN_BRACKET:
            context.push(ParserState::HANDLING_BRACKETS, ParserToken::from(token));
            break;
        case TokenizerTokenType::OPEN_CURLY_BRACE:
            context.push(ParserState::HANDLING_CURLY_BRACES, ParserToken::from(token));
            break;
        case TokenizerTokenType::COLON:
            context.push(ParserState::STARTING_INDENTED_BLOCK);
            break;

        case TokenizerTokenType::CLOSE_PARENTHESIS:
        case TokenizerTokenType::CLOSE_CURLY_BRACE:
        case TokenizerTokenType::CLOSE_BRACKET:
            throw context.closingUnopenedBlockException(ParserToken::from(token));
        
        default:
            throw context.exception("unexpected tokenizer token type encounted");
    };
}

} // namespace states
} // namespace parser
} // namespace yapllang
} // namespace org
