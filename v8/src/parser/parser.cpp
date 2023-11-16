#include "parser.hpp"
#include "lexer/tokenizer/tokenizer.hpp"
#include "parser_exception.hpp"

namespace org {
namespace yapllang {
namespace parser {

using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;

// #TokenizerTokenTypeNamesNeedToBeKeptInSync
const std::string parserTokenTypeNames[] = { 
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
        case TokenizerTokenType::QUOTED_STRING:
            return ParserTokenType::QUOTED_STRING;
        case TokenizerTokenType::ESCAPED_CHARACTER:
            return ParserTokenType::ESCAPED_CHARACTER;
        case TokenizerTokenType::MULTI_LINE_STRING:
            return ParserTokenType::MULTI_LINE_STRING;
        case TokenizerTokenType::COLON:
            return ParserTokenType::COLON;
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
        case TokenizerTokenType::MINUS_MINUS:
            return ParserTokenType::MINUS_MINUS;
        case TokenizerTokenType::MINUS_MINUS_MINUS:
            return ParserTokenType::MINUS_MINUS_MINUS;
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
