#include "handling_normal_stuff.hpp"
 
namespace org {
namespace yapllang {
namespace lexer {
namespace parser {
namespace states {

void handlingNormalStuff(const tokenizer::TokenizerToken &token, ParserContext& context) {
    switch (token.type) {
        case tokenizer::TokenizerTokenType::NORMAL:
            context.pushOutputToken(token);
            break;

        case tokenizer::TokenizerTokenType::COMMA:
            {
                // Commas have no special meaning within a normal/default section of YAPL
                tokenizer::TokenizerToken newToken(token);
                newToken.type = tokenizer::TokenizerTokenType::NORMAL;
                context.pushOutputToken(newToken);
            }
            break;

        case tokenizer::TokenizerTokenType::ESCAPED_CHARACTER:
            throw context.invalidTokenInThisContextException(token, ParserState::HANDLING_NORMAL_STUFF, "An escaped-character token is not expected as a token within a normal-block");

        case tokenizer::TokenizerTokenType::MINUS_MINUS_MINUS:
            // comment-line-separators are expected, but ignored
            break;

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
            context.push(ParserState::HANDLING_PARENTHESIS, token);
            break;
        case tokenizer::TokenizerTokenType::OPEN_BRACKET:
            context.push(ParserState::HANDLING_BRACKETS, token);
            break;
        case tokenizer::TokenizerTokenType::OPEN_CURLY_BRACE:
            context.push(ParserState::HANDLING_CURLY_BRACES, token);
            break;
        case tokenizer::TokenizerTokenType::COLON:
            context.push(ParserState::STARTING_INDENTED_BLOCK);
            break;

        case tokenizer::TokenizerTokenType::CLOSE_PARENTHESIS:
        case tokenizer::TokenizerTokenType::CLOSE_CURLY_BRACE:
        case tokenizer::TokenizerTokenType::CLOSE_BRACKET:
            throw context.closingUnopenedBlockException(token);
        
        default:
            throw context.exception("unexpected tokenizer token type encounted");
    };
}

} // namespace states
} // namespace parser
} // namespace lexer
} // namespace yapllang
} // namespace org
