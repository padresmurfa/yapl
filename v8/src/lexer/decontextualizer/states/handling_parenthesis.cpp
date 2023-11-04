#include "handling_parenthesis.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {
namespace states {

void handlingParenthesis(const preprocessor::PreprocessorToken &token, DecontextualizerContext& context) {
    switch (token.type) {
        case preprocessor::PreprocessorTokenType::CLOSE_PARENTHESIS:
            {
                context.pop(DecontextualizerState::HANDLING_PARENTHESIS, token);
            }
            break;

        case preprocessor::PreprocessorTokenType::ESCAPED_CHARACTER:
            throw context.invalidTokenInThisContextException(token, DecontextualizerState::HANDLING_PARENTHESIS, "An escaped character is not expected as a token within a parenthesis-block");

        case preprocessor::PreprocessorTokenType::COLON:
            throw context.invalidTokenInThisContextException(token, DecontextualizerState::HANDLING_PARENTHESIS, "A colon is not expected as a token within a parenthesis-block");

        case preprocessor::PreprocessorTokenType::CLOSE_CURLY_BRACE:
            throw context.closingUnopenedBlockException(token);

        case preprocessor::PreprocessorTokenType::END_MULTI_LINE_COMMENT:
            throw context.closingUnopenedBlockException(token);

        case preprocessor::PreprocessorTokenType::CLOSE_BRACKET:
            throw context.closingUnopenedBlockException(token);

        case preprocessor::PreprocessorTokenType::SEMICOLON:
            throw context.invalidTokenInThisContextException(token, DecontextualizerState::HANDLING_PARENTHESIS, "A semicolon token is not expected as a token within a parenthesis-block");

        case preprocessor::PreprocessorTokenType::SINGLE_LINE_COMMENT:
            context.push(DecontextualizerState::HANDLING_SINGLE_LINE_COMMENT, token);
            break;

        case preprocessor::PreprocessorTokenType::BEGIN_MULTI_LINE_COMMENT:
            context.push(DecontextualizerState::HANDLING_MULTI_LINE_COMMENT, token);
            break;

        case preprocessor::PreprocessorTokenType::QUOTED_STRING:
            {
                preprocessor::PreprocessorToken newToken(token);
                newToken.type = preprocessor::PreprocessorTokenType::BEGIN_QUOTED_STRING;
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

        case preprocessor::PreprocessorTokenType::NORMAL:
        case preprocessor::PreprocessorTokenType::COMMA:
            context.pushOutputToken(token);
            break;

        default:
            throw context.exception("unexpected preprocessor token type encounted");
    };
}

} // namespace states
} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org
