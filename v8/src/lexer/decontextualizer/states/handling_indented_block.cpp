#include "handling_indented_block.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {
namespace states {

void handlingIndentedBlock(const preprocessor::PreprocessorToken &token, DecontextualizerContext& context) {
    // TODO: identical to normal stuff, fix the duplication
    switch (token.type) {
       case preprocessor::PreprocessorTokenType::NORMAL:
            context.pushOutputToken(token);
            break;

        case preprocessor::PreprocessorTokenType::COMMA:
            {
                // Commas have no special meaning within a normal/default section of YAPL
                preprocessor::PreprocessorToken newToken(token);
                newToken.type = preprocessor::PreprocessorTokenType::NORMAL;
                context.pushOutputToken(newToken);
            }
            break;

        case preprocessor::PreprocessorTokenType::ESCAPED_CHARACTER:
            throw context.invalidTokenInThisContextException(token, DecontextualizerState::HANDLING_NORMAL_STUFF, "An escaped-character token is not expected as a token within a normal-block");

        case preprocessor::PreprocessorTokenType::MINUS_MINUS_MINUS:
            // commen-line-separators are expected, but ignored
            break;

        case preprocessor::PreprocessorTokenType::MINUS_MINUS:
            {
                preprocessor::PreprocessorToken newToken(token);
                newToken.type = preprocessor::PreprocessorTokenType::BEGIN_SINGLE_LINE_COMMENT;
                context.push(DecontextualizerState::HANDLING_SINGLE_LINE_COMMENT, newToken);
            }
            break;

        case preprocessor::PreprocessorTokenType::QUOTED_STRING:
            {
                preprocessor::PreprocessorToken newToken(token);
                newToken.type = preprocessor::PreprocessorTokenType::BEGIN_SINGLE_LINE_STRING;
                context.push(DecontextualizerState::HANDLING_QUOTED_STRING, newToken);
            }
            break;
        case preprocessor::PreprocessorTokenType::MULTI_LINE_STRING:
            {
                preprocessor::PreprocessorToken newToken(token);
                newToken.type = preprocessor::PreprocessorTokenType::BEGIN_MULTI_LINE_STRING;
                context.push(DecontextualizerState::HANDLING_MULTI_LINE_STRING, newToken);
            }
            break;
        case preprocessor::PreprocessorTokenType::OPEN_PARENTHESIS:
            context.push(DecontextualizerState::HANDLING_PARENTHESIS, token);
            break;
        case preprocessor::PreprocessorTokenType::OPEN_BRACKET:
            context.push(DecontextualizerState::HANDLING_BRACKETS, token);
            break;
        case preprocessor::PreprocessorTokenType::OPEN_CURLY_BRACE:
            context.push(DecontextualizerState::HANDLING_CURLY_BRACES, token);
            break;
        case preprocessor::PreprocessorTokenType::COLON:
            context.push(DecontextualizerState::STARTING_INDENTED_BLOCK, token);
            break;

        case preprocessor::PreprocessorTokenType::CLOSE_PARENTHESIS:
        case preprocessor::PreprocessorTokenType::CLOSE_CURLY_BRACE:
        case preprocessor::PreprocessorTokenType::CLOSE_BRACKET:
            throw context.closingUnopenedBlockException(token);
        
        default:
            throw context.exception("unexpected preprocessor token type encounted");
    };
}

} // namespace states
} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org
