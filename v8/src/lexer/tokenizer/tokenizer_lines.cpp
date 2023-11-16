#include "tokenizer_lines.hpp"
#include "lexer/file_reader/file_lines.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace tokenizer {

TokenizerLines::TokenizerLines() {
}

TokenizerLines::TokenizerLines(const TokenizerLines& other)
    : lines_(other.lines_)
{
}

TokenizerLines& TokenizerLines::operator=(const TokenizerLines& other) {
    if (this != &other) {
        lines_ = other.lines_;
    }
    return *this;   
}

void TokenizerLines::addLine(const TokenizerLine& line) {
    lines_.emplace_back(line);
}

TokenizerLines::iterator TokenizerLines::begin() const {
    return lines_.begin();
}

TokenizerLines::iterator TokenizerLines::end() const {
    return lines_.end();
}

TokenizerLine TokenizerLines::getEOFAsTokenizerLine() const {
    return lines_.rbegin()->atEOF();
}

TokenizerLines TokenizerLines::tokenize(const lexer::file_reader::FileLines& lines) {
    TokenizerLines lineTokens;
    for (auto line : lines) {
        TokenizerLine currentLineTokens(line);
        lineTokens.addLine(currentLineTokens);
    }
    return lineTokens;
}

void TokenizerLines::print() const {

    // Print the tokens per line
    for (const TokenizerLine& line : lines_) {
        if (line.empty()) {
            continue;
        }
        std::cout
            << "=============================================" << std::endl
            << "\"" << line.getLineWithoutWhitespace() << "\"" << std::endl
            << "FileLine " << line.getFileLine().getFileLocation().toString()
            << " Leading Whitespace: " << line.getLeadingWhitespace().size()
            << " Tokens: " << std::endl;
        // #TokenizerTokenTypeNamesNeedToBeKeptInSync
        for (const TokenizerToken& token : line.getTokens()) {
            switch (token.type) {
                case TokenizerTokenType::QUOTED_STRING:
                    std::cout << "  QUOTED_STRING: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::ESCAPED_CHARACTER:
                    std::cout << "  ESCAPED_CHARACTER: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::MULTI_LINE_STRING:
                    std::cout << "  MULTI_LINE_STRING: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::COLON:
                    std::cout << "  COLON: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::OPEN_PARENTHESIS:
                    std::cout << "  OPEN_PARENTHESIS: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::CLOSE_PARENTHESIS:
                    std::cout << "  CLOSE_PARENTHESIS: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::OPEN_BRACKET:
                    std::cout << "  OPEN_BRACKET: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::CLOSE_BRACKET:
                    std::cout << "  CLOSE_BRACKET: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::OPEN_CURLY_BRACE:
                    std::cout << "  OPEN_CURLY_BRACE: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::CLOSE_CURLY_BRACE:
                    std::cout << "  CLOSE_CURLY_BRACE: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::COMMA:
                    std::cout << "  COMMA: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::MINUS_MINUS:
                    std::cout << "  MINUS_MINUS: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::MINUS_MINUS_MINUS:
                    std::cout << "  MINUS_MINUS_MINUS: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::NORMAL:
                    std::cout << "  NORMAL: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::COMMENT_CONTENT:
                    std::cout << "  COMMENT_CONTENT: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::STRING_CONTENT:
                    std::cout << "  STRING_CONTENT: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::BEGIN_SINGLE_LINE_STRING:
                    std::cout << "  BEGIN_SINGLE_LINE_STRING: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::END_SINGLE_LINE_STRING:
                    std::cout << "  END_SINGLE_LINE_STRING: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::BEGIN_MULTI_LINE_STRING:
                    std::cout << "  BEGIN_MULTI_LINE_STRING: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::END_MULTI_LINE_STRING:
                    std::cout << "  END_MULTI_LINE_STRING: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::BEGIN_BLOCK:
                    std::cout << "  BEGIN_BLOCK: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::END_BLOCK:
                    std::cout << "  END_BLOCK: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::BEGIN_SINGLE_LINE_COMMENT:
                    std::cout << "  BEGIN_SINGLE_LINE_COMMENT: " << token.text << std::endl;
                    break;
                case TokenizerTokenType::END_SINGLE_LINE_COMMENT:
                    std::cout << "  END_SINGLE_LINE_COMMENT: " << token.text << std::endl;
                    break;
                default:
                    throw Exception("oops");
            }
        }
    }
}

} // namespace tokenizer
} // namespace lexer
} // namespace yapllang
} // namespace org
