#include "decontextualizer_line.hpp"
#include "lexer/file_reader/file_line.hpp"
#include "decontextualizer_exception.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {

using namespace org::yapllang;

DecontextualizerLine::DecontextualizerLine() {
}

DecontextualizerLine::DecontextualizerLine(
        const lexer::preprocessor::PreprocessorLine& line,
        const std::vector<preprocessor::PreprocessorToken> &tokens)
    : preprocessorLine_(line)
    , tokens_(tokens) {
}

DecontextualizerLine::DecontextualizerLine(const DecontextualizerLine& other)
    : preprocessorLine_(other.preprocessorLine_)
    , tokens_(other.tokens_)
{
}

DecontextualizerLine& DecontextualizerLine::operator=(const DecontextualizerLine& other) {
    if (this != &other) {
        preprocessorLine_ = other.preprocessorLine_;
        tokens_ = other.tokens_;
    }
    return *this;   
}

bool DecontextualizerLine::empty() const {
    return tokens_.empty();
}

const lexer::file_reader::FileLocation& DecontextualizerLine::getFileLocation() const {
    return preprocessorLine_.getFileLocation();
}

const lexer::preprocessor::PreprocessorLine& DecontextualizerLine::getPreprocessorLine() const {
    return preprocessorLine_;    
}

const std::vector<preprocessor::PreprocessorToken>& DecontextualizerLine::getTokens() const {
    return tokens_;
}

std::string DecontextualizerLine::toString() const {
    std::stringstream ss;
    ss
        << "=============================================" << std::endl
        << "PreprocessorLine: " << preprocessorLine_.toString()  << std::endl
        << "---------"  << std::endl
        << " Decontextualized Tokens: " << std::endl;

    using preprocessor::PreprocessorToken;
    using preprocessor::PreprocessorTokenType;
    // #PreprocessorTokenTypeNamesNeedToBeKeptInSync
    for (const PreprocessorToken& token : getTokens()) {
        switch (token.type) {
            case PreprocessorTokenType::SINGLE_LINE_COMMENT:
                ss << "  SINGLE_LINE_COMMENT: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::SEMICOLON:
                ss << "  SEMICOLON: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::BEGIN_MULTI_LINE_COMMENT:
                ss << "  BEGIN_MULTI_LINE_COMMENT: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::END_MULTI_LINE_COMMENT:
                ss << "  END_MULTI_LINE_COMMENT: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::QUOTED_STRING:
                ss << "  QUOTED_STRING: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::ESCAPED_CHARACTER:
                ss << "  ESCAPED_CHARACTER: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::MULTI_LINE_STRING:
                ss << "  MULTI_LINE_STRING: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::COLON:
                ss << "  COLON: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::OPEN_PARENTHESIS:
                ss << "  OPEN_PARENTHESIS: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::CLOSE_PARENTHESIS:
                ss << "  CLOSE_PARENTHESIS: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::OPEN_BRACKET:
                ss << "  OPEN_BRACKET: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::CLOSE_BRACKET:
                ss << "  CLOSE_BRACKET: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::OPEN_CURLY_BRACE:
                ss << "  OPEN_CURLY_BRACE: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::CLOSE_CURLY_BRACE:
                ss << "  CLOSE_CURLY_BRACE: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::COMMA:
                ss << "  COMMA: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::NORMAL:
                ss << "  NORMAL: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::COMMENT_OR_STRING_CONTENT:
                ss << "  COMMENT_OR_STRING_CONTENT: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::BEGIN_QUOTED_STRING:
                ss << "  BEGIN_QUOTED_STRING: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::END_QUOTED_STRING:
                ss << "  END_QUOTED_STRING: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::BEGIN_MULTI_LINE_STRING:
                ss << "  BEGIN_MULTI_LINE_STRING: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::END_MULTI_LINE_STRING:
                ss << "  END_MULTI_LINE_STRING: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::BEGIN_BLOCK:
                ss << "  BEGIN_BLOCK: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::END_BLOCK:
                ss << "  END_BLOCK: " << token.text << std::endl;
                break;
            default:
                throw DecontextualizerException("oops");
        }
    }
    return ss.str();    
}


} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org
