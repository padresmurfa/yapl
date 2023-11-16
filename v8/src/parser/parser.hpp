#pragma once

#ifndef ORG_YAPLLANG_PARSER_HPP
#define ORG_YAPLLANG_PARSER_HPP

#include "include.hpp"
#include "lexer/file_reader/file_location.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace tokenizer {
    struct TokenizerToken;
}
}
namespace parser {

// ##TokenizerTokenTypeNamesNeedToBeKeptInSync
// When updating this code, make sure that you keep 'tokenizerTokenTypeNames' in sync
enum class ParserTokenType {
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
    MINUS_MINUS_MINUS,

    // parser token types
    COMMENT_CONTENT,
    STRING_CONTENT,
    BEGIN_SINGLE_LINE_STRING,
    END_SINGLE_LINE_STRING,
    BEGIN_MULTI_LINE_STRING,
    END_MULTI_LINE_STRING,
    BEGIN_BLOCK,
    END_BLOCK,
    BEGIN_SINGLE_LINE_COMMENT,
    END_SINGLE_LINE_COMMENT
};


class ParserToken {
public:
    ParserTokenType type;
    std::string text;
    lexer::file_reader::FileLocation location;

    std::string toString() const;
    static ParserToken from(const lexer::tokenizer::TokenizerToken &token);
    static ParserToken from(const lexer::tokenizer::TokenizerToken &token, ParserTokenType type);
};


} // namespace parser
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PARSER_HPP
