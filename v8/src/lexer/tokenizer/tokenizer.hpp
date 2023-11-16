#pragma once

#ifndef ORG_YAPLLANG_TOKENIZER_HPP
#define ORG_YAPLLANG_TOKENIZER_HPP

#include "include.hpp"
#include "lexer/file_reader/file_location.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace tokenizer {

// ##TokenizerTokenTypeNamesNeedToBeKeptInSync
// When updating this code, make sure that you keep 'tokenizerTokenTypeNames' in sync
enum class TokenizerTokenType {
    NORMAL,
    QUOTED_STRING,
    ESCAPED_CHARACTER, // TODO: add support for \UHHHHHHHH
    MULTI_LINE_STRING,
    COLON,
    OPEN_PARENTHESIS,
    CLOSE_PARENTHESIS,
    OPEN_BRACKET,
    CLOSE_BRACKET,
    OPEN_CURLY_BRACE,
    CLOSE_CURLY_BRACE,
    COMMA,
    MINUS_MINUS,
    MINUS_MINUS_MINUS
};


struct TokenizerToken {
    TokenizerTokenType type;
    std::string text;
    lexer::file_reader::FileLocation location;

    std::string toString() const;
};


} // namespace tokenizer
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_TOKENIZER_HPP
