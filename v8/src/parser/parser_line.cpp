#include "parser_line.hpp"
#include "lexer/file_reader/file_line.hpp"
#include "parser_exception.hpp"

namespace org {
namespace yapllang {
namespace parser {

using namespace org::yapllang;
using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;

ParserLine::ParserLine() {
}

ParserLine::ParserLine(
        const lexer::tokenizer::TokenizerLine& line,
        const std::vector<ParserToken> &tokens)
    : tokenizerLine_(line)
    , tokens_(tokens) {
}

ParserLine::ParserLine(const ParserLine& other)
    : tokenizerLine_(other.tokenizerLine_)
    , tokens_(other.tokens_)
{
}

ParserLine& ParserLine::operator=(const ParserLine& other) {
    if (this != &other) {
        tokenizerLine_ = other.tokenizerLine_;
        tokens_ = other.tokens_;
    }
    return *this;   
}

bool ParserLine::empty() const {
    return tokens_.empty();
}

const lexer::file_reader::FileLocation& ParserLine::getFileLocation() const {
    return tokenizerLine_.getFileLocation();
}

const lexer::tokenizer::TokenizerLine& ParserLine::getTokenizerLine() const {
    return tokenizerLine_;    
}

const std::vector<ParserToken>& ParserLine::getTokens() const {
    return tokens_;
}

std::vector<ParserToken>& ParserLine::mutateTokens() {
    return tokens_;
}

std::string maybeValue(const ParserToken &token, const std::string &expected) {
    if (token.text != expected) {
        return "(value='" + token.text + "')";
    }
    return "";
}

std::string ParserLine::toString() const {
    std::stringstream ss;
/*    ss
        << "=============================================" << std::endl
        << "TokenizerLine: " << tokenizerLine_.toString()  << std::endl
        << "---------"  << std::endl
        << " Parsed Tokens: " << std::endl;
*/
    // #ParserTokenTypeNamesNeedToBeKeptInSync
    for (const ParserToken& token : getTokens()) {
        switch (token.type) {
            case ParserTokenType::OPEN_PARENTHESIS:
                ss << "  OPEN_PARENTHESIS" << maybeValue(token, "(");
                break;
            case ParserTokenType::CLOSE_PARENTHESIS:
                ss << "  CLOSE_PARENTHESIS" << maybeValue(token, ")");
                break;
            case ParserTokenType::OPEN_BRACKET:
                ss << "  OPEN_BRACKET" << maybeValue(token, "[");
                break;
            case ParserTokenType::CLOSE_BRACKET:
                ss << "  CLOSE_BRACKET" << maybeValue(token, "]");
                break;
            case ParserTokenType::OPEN_CURLY_BRACE:
                ss << "  OPEN_CURLY_BRACE" << maybeValue(token, "{");
                break;
            case ParserTokenType::CLOSE_CURLY_BRACE:
                ss << "  CLOSE_CURLY_BRACE" << maybeValue(token, "}");
                break;
            case ParserTokenType::COMMA:
                ss << "  COMMA" << maybeValue(token, ",");
                break;
            case ParserTokenType::NORMAL:
                ss << "  NORMAL" << maybeValue(token, "");
                break;
            case ParserTokenType::TMP_SINGLE_LINE_COMMENT_CONTENT:
                ss << "  TMP_SINGLE_LINE_COMMENT_CONTENT" << maybeValue(token, "");
                break;
            case ParserTokenType::TMP_MULTI_LINE_COMMENT_CONTENT:
                ss << "  TMP_MULTI_LINE_COMMENT_CONTENT" << maybeValue(token, "");
                break;
            case ParserTokenType::STRING_CONTENT:
                ss << "  STRING_CONTENT" << maybeValue(token, "");
                break;
            case ParserTokenType::BEGIN_SINGLE_LINE_STRING:
                ss << "  BEGIN_SINGLE_LINE_STRING" << maybeValue(token, "");
                break;
            case ParserTokenType::END_SINGLE_LINE_STRING:
                ss << "  END_SINGLE_LINE_STRING" << maybeValue(token, "");
                break;
            case ParserTokenType::BEGIN_MULTI_LINE_STRING:
                ss << "  BEGIN_MULTI_LINE_STRING" << maybeValue(token, "");
                break;
            case ParserTokenType::END_MULTI_LINE_STRING:
                ss << "  END_MULTI_LINE_STRING" << maybeValue(token, "");
                break;
            case ParserTokenType::BEGIN_BLOCK:
                ss << "  BEGIN_BLOCK" << maybeValue(token, "");
                break;
            case ParserTokenType::END_BLOCK:
                ss << "  END_BLOCK" << maybeValue(token, "");
                break;
            case ParserTokenType::TMP_BEGIN_SINGLE_LINE_COMMENT:
                ss << "  TMP_BEGIN_SINGLE_LINE_COMMENT" << maybeValue(token, "");
                break;
            case ParserTokenType::TMP_END_SINGLE_LINE_COMMENT:
                ss << "  TMP_END_SINGLE_LINE_COMMENT" << maybeValue(token, "");
                break;
            case ParserTokenType::TMP_BEGIN_MULTI_LINE_COMMENT:
                ss << "  TMP_BEGIN_MULTI_LINE_COMMENT" << maybeValue(token, "");
                break;
            case ParserTokenType::TMP_END_MULTI_LINE_COMMENT:
                ss << "  TMP_END_MULTI_LINE_COMMENT" << maybeValue(token, "");
                break;
            case ParserTokenType::COMMENT:
                ss << "  COMMENT" << maybeValue(token, "");
                break;
            default:
                throw ParserException("oops");
        }
    }
    ss << std::endl;
    return ss.str();    
}


} // namespace parser
} // namespace yapllang
} // namespace org
