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
    "MINUS_MINUS_MINUS"
 };

std::string TokenizerToken::toString() const {
    std::string typeStr = tokenizerTokenTypeNames[static_cast<int>(type)];
    return std::string("TokenizerToken (type=" + typeStr + ", text=\"" + text + "\", location=\"" + location.toString() + "\")");
}

} // namespace tokenizer
} // namespace lexer
} // namespace yapllang
} // namespace org
