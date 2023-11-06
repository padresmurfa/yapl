#include "handling_single_line_comment.hpp"
 
namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {
namespace states {

void handlingSingleLineComment(const preprocessor::PreprocessorToken &token, DecontextualizerContext& context) {
    switch (token.type) {
        case preprocessor::PreprocessorTokenType::NORMAL:
        case preprocessor::PreprocessorTokenType::COMMA:
        case preprocessor::PreprocessorTokenType::MINUS_MINUS:
        case preprocessor::PreprocessorTokenType::MINUS_MINUS_MINUS:
        case preprocessor::PreprocessorTokenType::QUOTED_STRING:
        case preprocessor::PreprocessorTokenType::ESCAPED_CHARACTER:
        case preprocessor::PreprocessorTokenType::MULTI_LINE_STRING:
        case preprocessor::PreprocessorTokenType::OPEN_PARENTHESIS:
        case preprocessor::PreprocessorTokenType::OPEN_BRACKET:
        case preprocessor::PreprocessorTokenType::OPEN_CURLY_BRACE:
        case preprocessor::PreprocessorTokenType::COLON:
        case preprocessor::PreprocessorTokenType::CLOSE_PARENTHESIS:
        case preprocessor::PreprocessorTokenType::CLOSE_CURLY_BRACE:
        case preprocessor::PreprocessorTokenType::CLOSE_BRACKET:
            {
                // nothing has a special meaning within a single-line comment in YAPL
                preprocessor::PreprocessorToken newToken(token);
                newToken.type = preprocessor::PreprocessorTokenType::COMMENT_OR_STRING_CONTENT;
                context.pushOutputToken(newToken);
            }
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
