#include "parser.hpp"
#include "lexer/tokenizer/tokenizer.hpp"
#include "parser_exception.hpp"

namespace org {
namespace yapllang {
namespace parser {

using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;

// #ParserTokenTypeNamesNeedToBeKeptInSync
const std::string parserTokenTypeNames[] = { 
    "NORMAL",
    "OPEN_PARENTHESIS",
    "CLOSE_PARENTHESIS",
    "OPEN_BRACKET",
    "CLOSE_BRACKET",
    "OPEN_CURLY_BRACE",
    "CLOSE_CURLY_BRACE",
    "COMMA",

    "SINGLE_LINE_COMMENT_CONTENT",
    "MULTI_LINE_COMMENT_CONTENT",
    "STRING_CONTENT",
    "BEGIN_SINGLE_LINE_STRING",
    "END_SINGLE_LINE_STRING",
    "BEGIN_MULTI_LINE_STRING",
    "END_MULTI_LINE_STRING",
    "BEGIN_BLOCK",
    "END_BLOCK",
    "BEGIN_SINGLE_LINE_COMMENT",
    "END_SINGLE_LINE_COMMENT",
    "BEGIN_MULTI_LINE_COMMENT",
    "END_MULTI_LINE_COMMENT"
 };

std::string ParserToken::toString() const {
    std::string typeStr = parserTokenTypeNames[static_cast<int>(type)];
    return std::string("ParserToken (type=" + typeStr + ", text=\"" + text + "\", location=\"" + location.toString() + "\")");
}

ParserToken ParserToken::from(const lexer::tokenizer::TokenizerToken &token, ParserTokenType type) {
    ParserToken result;
    result.text = token.text;
    result.location = token.location;
    result.type = type;
    return result;
}

ParserTokenType tokenizerTokenTypeToParserTokenType(lexer::tokenizer::TokenizerTokenType tokenizerTokenType) {
    switch (tokenizerTokenType) {
        case TokenizerTokenType::OPEN_PARENTHESIS:
            return ParserTokenType::OPEN_PARENTHESIS;
        case TokenizerTokenType::CLOSE_PARENTHESIS:
            return ParserTokenType::CLOSE_PARENTHESIS;
        case TokenizerTokenType::OPEN_BRACKET:
            return ParserTokenType::OPEN_BRACKET;
        case TokenizerTokenType::CLOSE_BRACKET:
            return ParserTokenType::CLOSE_BRACKET;
        case TokenizerTokenType::OPEN_CURLY_BRACE:
            return ParserTokenType::OPEN_CURLY_BRACE;
        case TokenizerTokenType::CLOSE_CURLY_BRACE:
            return ParserTokenType::CLOSE_CURLY_BRACE;
        case TokenizerTokenType::COMMA:
            return ParserTokenType::COMMA;
        case TokenizerTokenType::NORMAL:
            return ParserTokenType::NORMAL;
        default:
            throw ParserException("oops");
    }
}

ParserToken ParserToken::from(const TokenizerToken &token) {
    ParserToken result;
    result.text = token.text;
    result.location = token.location;
    result.type = tokenizerTokenTypeToParserTokenType(token.type);
    return result;
};


} // namespace parser
} // namespace yapllang
} // namespace org
