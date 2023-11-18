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
                ss << "  OPEN_PARENTHESIS: " << token.text << std::endl;
                break;
            case ParserTokenType::CLOSE_PARENTHESIS:
                ss << "  CLOSE_PARENTHESIS: " << token.text << std::endl;
                break;
            case ParserTokenType::OPEN_BRACKET:
                ss << "  OPEN_BRACKET: " << token.text << std::endl;
                break;
            case ParserTokenType::CLOSE_BRACKET:
                ss << "  CLOSE_BRACKET: " << token.text << std::endl;
                break;
            case ParserTokenType::OPEN_CURLY_BRACE:
                ss << "  OPEN_CURLY_BRACE: " << token.text << std::endl;
                break;
            case ParserTokenType::CLOSE_CURLY_BRACE:
                ss << "  CLOSE_CURLY_BRACE: " << token.text << std::endl;
                break;
            case ParserTokenType::COMMA:
                ss << "  COMMA: " << token.text << std::endl;
                break;
            case ParserTokenType::NORMAL:
                ss << "  NORMAL: " << token.text << std::endl;
                break;
            case ParserTokenType::SINGLE_LINE_COMMENT_CONTENT:
                ss << "  SINGLE_LINE_COMMENT_CONTENT: " << token.text << std::endl;
                break;
            case ParserTokenType::MULTI_LINE_COMMENT_CONTENT:
                ss << "  MULTI_LINE_COMMENT_CONTENT: " << token.text << std::endl;
                break;
            case ParserTokenType::STRING_CONTENT:
                ss << "  STRING_CONTENT: " << token.text << std::endl;
                break;
            case ParserTokenType::BEGIN_SINGLE_LINE_STRING:
                ss << "  BEGIN_SINGLE_LINE_STRING: " << token.text << std::endl;
                break;
            case ParserTokenType::END_SINGLE_LINE_STRING:
                ss << "  END_SINGLE_LINE_STRING: " << token.text << std::endl;
                break;
            case ParserTokenType::BEGIN_MULTI_LINE_STRING:
                ss << "  BEGIN_MULTI_LINE_STRING: " << token.text << std::endl;
                break;
            case ParserTokenType::END_MULTI_LINE_STRING:
                ss << "  END_MULTI_LINE_STRING: " << token.text << std::endl;
                break;
            case ParserTokenType::BEGIN_BLOCK:
                ss << "  BEGIN_BLOCK: " << token.text << std::endl;
                break;
            case ParserTokenType::END_BLOCK:
                ss << "  END_BLOCK: " << token.text << std::endl;
                break;
            case ParserTokenType::BEGIN_SINGLE_LINE_COMMENT:
                ss << "  BEGIN_SINGLE_LINE_COMMENT: " << token.text << std::endl;
                break;
            case ParserTokenType::END_SINGLE_LINE_COMMENT:
                ss << "  END_SINGLE_LINE_COMMENT: " << token.text << std::endl;
                break;
            case ParserTokenType::BEGIN_MULTI_LINE_COMMENT:
                ss << "  BEGIN_MULTI_LINE_COMMENT: " << token.text << std::endl;
                break;
            case ParserTokenType::END_MULTI_LINE_COMMENT:
                ss << "  END_MULTI_LINE_COMMENT: " << token.text << std::endl;
                break;
            default:
                throw ParserException("oops");
        }
    }
    return ss.str();    
}


} // namespace parser
} // namespace yapllang
} // namespace org
