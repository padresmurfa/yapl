#include "handling_multi_line_string.hpp"
#include "unescape_character.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {
namespace states {

void handlingMultiLineString(const preprocessor::PreprocessorToken &token, DecontextualizerContext& context) {
    switch (token.type) {
        case preprocessor::PreprocessorTokenType::MULTI_LINE_STRING:
            {
                preprocessor::PreprocessorToken newToken(token);
                newToken.type = preprocessor::PreprocessorTokenType::END_QUOTED_STRING;
                context.push(DecontextualizerState::HANDLING_QUOTED_STRING, newToken);
            }
            break;

        case preprocessor::PreprocessorTokenType::ESCAPED_CHARACTER:
            {
                preprocessor::PreprocessorToken newToken(token);
                newToken.type = preprocessor::PreprocessorTokenType::COMMENT_OR_STRING_CONTENT;
                newToken.text = unescapeCharacter(newToken.text.substr(1), newToken);
                context.pushOutputToken(newToken);
            }
            break;

        case preprocessor::PreprocessorTokenType::NORMAL:
        case preprocessor::PreprocessorTokenType::COMMA:
        case preprocessor::PreprocessorTokenType::SINGLE_LINE_COMMENT:
        case preprocessor::PreprocessorTokenType::SEMICOLON:
        case preprocessor::PreprocessorTokenType::BEGIN_MULTI_LINE_COMMENT:
        case preprocessor::PreprocessorTokenType::END_MULTI_LINE_COMMENT:
        case preprocessor::PreprocessorTokenType::QUOTED_STRING:
        case preprocessor::PreprocessorTokenType::OPEN_PARENTHESIS:
        case preprocessor::PreprocessorTokenType::OPEN_BRACKET:
        case preprocessor::PreprocessorTokenType::OPEN_CURLY_BRACE:
        case preprocessor::PreprocessorTokenType::COLON:
        case preprocessor::PreprocessorTokenType::CLOSE_PARENTHESIS:
        case preprocessor::PreprocessorTokenType::CLOSE_CURLY_BRACE:
        case preprocessor::PreprocessorTokenType::CLOSE_BRACKET:
            {
                // nothing (except */)) has a special meaning within a multi-line comment in YAPL
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
