#include "preprocessor.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace preprocessor {

// #PreprocessorTokenTypeNamesNeedToBeKeptInSync
const std::string preprocessorTokenTypeNames[] = { 
    "NORMAL",
    "QUOTED_STRING",
    "ESCAPED_CHARACTER",
    "MULTI_LINE_STRING",
    "COLON",
    "OPEN_PARENTHESIS",
    "CLOSE_PARENTHESIS",
    "OPEN_BRACKET",
    "CLOSE_BRACKET",
    "OPEN_CURLY_BRACE",
    "CLOSE_CURLY_BRACE",
    "COMMA",
    "MINUS_MINUS",
    "MINUS_MINUS_MINUS",

    "COMMENT_OR_STRING_CONTENT",
    "BEGIN_SINGLE_LINE_STRING",
    "END_SINGLE_LINE_STRING",
    "BEGIN_MULTI_LINE_STRING",
    "END_MULTI_LINE_STRING",
    "BEGIN_BLOCK",
    "END_BLOCK",
    "BEGIN_SINGLE_LINE_COMMENT",
    "END_SINGLE_LINE_COMMENT",
 };

std::string PreprocessorToken::toString() const {
    std::string typeStr = preprocessorTokenTypeNames[static_cast<int>(type)];
    return std::string("PreprocessorToken (type=" + typeStr + ", text=\"" + text + "\", location=\"" + location.toString() + "\")");
}

} // namespace preprocessor
} // namespace lexer
} // namespace yapllang
} // namespace org
