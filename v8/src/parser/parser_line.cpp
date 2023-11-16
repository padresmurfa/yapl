#include "parser_line.hpp"
#include "lexer/file_reader/file_line.hpp"
#include "parser_exception.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace parser {

using namespace org::yapllang;

ParserLine::ParserLine() {
}

ParserLine::ParserLine(
        const lexer::tokenizer::TokenizerLine& line,
        const std::vector<tokenizer::TokenizerToken> &tokens)
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

const std::vector<tokenizer::TokenizerToken>& ParserLine::getTokens() const {
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
    using tokenizer::TokenizerToken;
    using tokenizer::TokenizerTokenType;
    // #TokenizerTokenTypeNamesNeedToBeKeptInSync
    for (const TokenizerToken& token : getTokens()) {
        switch (token.type) {
            case TokenizerTokenType::QUOTED_STRING:
                ss << "  QUOTED_STRING: " << token.text << std::endl;
                break;
            case TokenizerTokenType::ESCAPED_CHARACTER:
                ss << "  ESCAPED_CHARACTER: " << token.text << std::endl;
                break;
            case TokenizerTokenType::MULTI_LINE_STRING:
                ss << "  MULTI_LINE_STRING: " << token.text << std::endl;
                break;
            case TokenizerTokenType::COLON:
                ss << "  COLON: " << token.text << std::endl;
                break;
            case TokenizerTokenType::OPEN_PARENTHESIS:
                ss << "  OPEN_PARENTHESIS: " << token.text << std::endl;
                break;
            case TokenizerTokenType::CLOSE_PARENTHESIS:
                ss << "  CLOSE_PARENTHESIS: " << token.text << std::endl;
                break;
            case TokenizerTokenType::OPEN_BRACKET:
                ss << "  OPEN_BRACKET: " << token.text << std::endl;
                break;
            case TokenizerTokenType::CLOSE_BRACKET:
                ss << "  CLOSE_BRACKET: " << token.text << std::endl;
                break;
            case TokenizerTokenType::OPEN_CURLY_BRACE:
                ss << "  OPEN_CURLY_BRACE: " << token.text << std::endl;
                break;
            case TokenizerTokenType::CLOSE_CURLY_BRACE:
                ss << "  CLOSE_CURLY_BRACE: " << token.text << std::endl;
                break;
            case TokenizerTokenType::COMMA:
                ss << "  COMMA: " << token.text << std::endl;
                break;
            case TokenizerTokenType::MINUS_MINUS:
                ss << "  MINUS_MINUS: " << token.text << std::endl;
                break;
            case TokenizerTokenType::MINUS_MINUS_MINUS:
                ss << "  MINUS_MINUS_MINUS: " << token.text << std::endl;
                break;
            case TokenizerTokenType::NORMAL:
                ss << "  NORMAL: " << token.text << std::endl;
                break;
            case TokenizerTokenType::COMMENT_CONTENT:
                ss << "  COMMENT_CONTENT: " << token.text << std::endl;
                break;
            case TokenizerTokenType::STRING_CONTENT:
                ss << "  STRING_CONTENT: " << token.text << std::endl;
                break;
            case TokenizerTokenType::BEGIN_SINGLE_LINE_STRING:
                ss << "  BEGIN_SINGLE_LINE_STRING: " << token.text << std::endl;
                break;
            case TokenizerTokenType::END_SINGLE_LINE_STRING:
                ss << "  END_SINGLE_LINE_STRING: " << token.text << std::endl;
                break;
            case TokenizerTokenType::BEGIN_MULTI_LINE_STRING:
                ss << "  BEGIN_MULTI_LINE_STRING: " << token.text << std::endl;
                break;
            case TokenizerTokenType::END_MULTI_LINE_STRING:
                ss << "  END_MULTI_LINE_STRING: " << token.text << std::endl;
                break;
            case TokenizerTokenType::BEGIN_BLOCK:
                ss << "  BEGIN_BLOCK: " << token.text << std::endl;
                break;
            case TokenizerTokenType::END_BLOCK:
                ss << "  END_BLOCK: " << token.text << std::endl;
                break;
            case TokenizerTokenType::BEGIN_SINGLE_LINE_COMMENT:
                ss << "  BEGIN_SINGLE_LINE_COMMENT: " << token.text << std::endl;
                break;
            case TokenizerTokenType::END_SINGLE_LINE_COMMENT:
                ss << "  END_SINGLE_LINE_COMMENT: " << token.text << std::endl;
                break;
            default:
                throw ParserException("oops");
        }
    }
    return ss.str();    
}


} // namespace parser
} // namespace lexer
} // namespace yapllang
} // namespace org
