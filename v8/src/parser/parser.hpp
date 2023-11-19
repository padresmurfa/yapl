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

// ##ParserTokenTypeNamesNeedToBeKeptInSync
// When updating this code, make sure that you keep 'parserTokenTypeNames' in sync
enum class ParserTokenType {
    NORMAL,
    OPEN_PARENTHESIS,
    CLOSE_PARENTHESIS,
    OPEN_BRACKET,
    CLOSE_BRACKET,
    OPEN_CURLY_BRACE,
    CLOSE_CURLY_BRACE,
    COMMA,

    // parser token types
    TMP_SINGLE_LINE_COMMENT_CONTENT,
    TMP_MULTI_LINE_COMMENT_CONTENT,
    STRING_CONTENT,
    BEGIN_SINGLE_LINE_STRING,
    END_SINGLE_LINE_STRING,
    BEGIN_MULTI_LINE_STRING,
    END_MULTI_LINE_STRING,
    BEGIN_BLOCK,
    END_BLOCK,
    TMP_BEGIN_SINGLE_LINE_COMMENT,
    TMP_END_SINGLE_LINE_COMMENT,
    TMP_BEGIN_MULTI_LINE_COMMENT,
    TMP_END_MULTI_LINE_COMMENT,
    COMMENT
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

void mergeToken(ParserToken& previousToken, const ParserToken& currentToken);
bool maybeMergeToken(ParserToken& previousToken, const ParserToken& currentToken);


} // namespace parser
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PARSER_HPP
