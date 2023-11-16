#include "tokenizer.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace tokenizer {

// #TokenizerTokenTypeNamesNeedToBeKeptInSync
const std::string tokenizerTokenTypeNames[] = { 
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

    "COMMENT_CONTENT",
    "STRING_CONTENT",
    "BEGIN_SINGLE_LINE_STRING",
    "END_SINGLE_LINE_STRING",
    "BEGIN_MULTI_LINE_STRING",
    "END_MULTI_LINE_STRING",
    "BEGIN_BLOCK",
    "END_BLOCK",
    "BEGIN_SINGLE_LINE_COMMENT",
    "END_SINGLE_LINE_COMMENT",
 };

std::string TokenizerToken::toString() const {
    std::string typeStr = tokenizerTokenTypeNames[static_cast<int>(type)];
    return std::string("TokenizerToken (type=" + typeStr + ", text=\"" + text + "\", location=\"" + location.toString() + "\")");
}

} // namespace tokenizer
} // namespace lexer
} // namespace yapllang
} // namespace org
