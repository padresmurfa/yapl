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

    "TMP_SINGLE_LINE_COMMENT_CONTENT",
    "TMP_MULTI_LINE_COMMENT_CONTENT",
    "TMP_STRING_CONTENT",
    "TMP_BEGIN_SINGLE_LINE_STRING",
    "TMP_END_SINGLE_LINE_STRING",
    "TMP_BEGIN_MULTI_LINE_STRING",
    "TMP_END_MULTI_LINE_STRING",
    "BEGIN_BLOCK",
    "END_BLOCK",
    "TMP_BEGIN_SINGLE_LINE_COMMENT",
    "TMP_END_SINGLE_LINE_COMMENT",
    "TMP_BEGIN_MULTI_LINE_COMMENT",
    "TMP_END_MULTI_LINE_COMMENT",
    "COMMENT",
    "STRING"
 };

std::string ParserToken::toString() const {
    std::string typeStr = parserTokenTypeNames[static_cast<int>(type)];
    return std::string("ParserToken (type=" + typeStr + ", text=\"" + text + "\", area=\"" + area.toString() + "\")");
}

bool ParserToken::isImmediatePredecessorOf(const ParserToken& other) const {
    return area.isImmediatePredecessorOf(other.area);
}

bool ParserToken::isPredecessorLineOf(const ParserToken& other) const {
    return area.isPredecessorLineOf(other.area);
}

ParserToken ParserToken::from(const lexer::tokenizer::TokenizerToken &token, ParserTokenType type) {
    ParserToken result;
    result.text = token.text;
    result.area = token.area;
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
    result.area = token.area;
    result.type = tokenizerTokenTypeToParserTokenType(token.type);
    return result;
};

void mergeToken(ParserToken& previousToken, const ParserToken& currentToken) {
    // TODO: consider ensuring that the end position of currentToken is available to previousToken, as
    // otherwise its not really possible to ensure that whoever is using our parse tree has totally
    // correct positioning information.
    previousToken.text.append(currentToken.text);
    previousToken.area = lexer::file_reader::FileArea(
        previousToken.area.getFilename(),
        previousToken.area.getBegin(),
        currentToken.area.getEnd()
    );
}

bool maybeMergeToken(ParserToken& previousToken, const ParserToken& currentToken) {
    if (previousToken.area.isImmediatePredecessorOf(currentToken.area)) {
        mergeToken(previousToken, currentToken);
        return true;
    }
    return false;
}

} // namespace parser
} // namespace yapllang
} // namespace org
