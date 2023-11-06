#include "handling_curly_braces.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {
namespace states {

void handlingCurlyBraces(const preprocessor::PreprocessorToken &token, DecontextualizerContext& context) {
    switch (token.type) {
        case preprocessor::PreprocessorTokenType::CLOSE_CURLY_BRACE:
            {
                context.pop(DecontextualizerState::HANDLING_CURLY_BRACES, token);
            }
            break;

        case preprocessor::PreprocessorTokenType::ESCAPED_CHARACTER:
            throw context.invalidTokenInThisContextException(token, DecontextualizerState::HANDLING_CURLY_BRACES, "An escaped character is not expected as a token within a curly-braces-block");

        case preprocessor::PreprocessorTokenType::COLON:
            // TODO: maps have forms like { a: b }
            throw context.invalidTokenInThisContextException(token, DecontextualizerState::HANDLING_CURLY_BRACES, "A colon is not expected as a token within a curly-braces-block");

        case preprocessor::PreprocessorTokenType::CLOSE_BRACKET:
            throw context.closingUnopenedBlockException(token);

        case preprocessor::PreprocessorTokenType::CLOSE_PARENTHESIS:
            throw context.closingUnopenedBlockException(token);

        case preprocessor::PreprocessorTokenType::MINUS_MINUS_MINUS:
            throw context.invalidTokenInThisContextException(token, DecontextualizerState::HANDLING_CURLY_BRACES, "A comment-line-separator token is not expected as a token within a curly-braces-block");

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
            context.push(DecontextualizerState::HANDLING_CURLY_BRACES, token);
            break;

        case preprocessor::PreprocessorTokenType::OPEN_BRACKET:
            context.push(DecontextualizerState::HANDLING_CURLY_BRACES, token);
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
