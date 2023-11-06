#pragma once

#ifndef ORG_YAPLLANG_PREPROCESSOR_HPP
#define ORG_YAPLLANG_PREPROCESSOR_HPP

#include "include.hpp"
#include "lexer/file_reader/file_location.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace preprocessor {

// ##PreprocessorTokenTypeNamesNeedToBeKeptInSync
// When updating this code, make sure that you keep 'preprocessorTokenTypeNames' in sync
enum class PreprocessorTokenType {
    NORMAL,
    QUOTED_STRING,
    ESCAPED_CHARACTER,
    // TODO: add support for \xHH, \uHHHH and \UHHHHHHHH
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
    MINUS_MINUS_MINUS,

    // decontextualizer token types
    COMMENT_OR_STRING_CONTENT,
    BEGIN_SINGLE_LINE_STRING,
    END_SINGLE_LINE_STRING,
    BEGIN_MULTI_LINE_STRING,
    END_MULTI_LINE_STRING,
    BEGIN_BLOCK,
    END_BLOCK,
    BEGIN_SINGLE_LINE_COMMENT,
    END_SINGLE_LINE_COMMENT
};


struct PreprocessorToken {
    PreprocessorTokenType type;
    std::string text;
    lexer::file_reader::FileLocation location;

    std::string toString() const;
};


} // namespace preprocessor
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PREPROCESSOR_HPP
