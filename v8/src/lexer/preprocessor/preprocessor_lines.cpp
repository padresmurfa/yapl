#include "preprocessor_lines.hpp"
#include "lexer/file_reader/file_lines.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace preprocessor {

PreprocessorLines::PreprocessorLines() {
}

PreprocessorLines::PreprocessorLines(const PreprocessorLines& other)
    : lines_(other.lines_)
{
}

PreprocessorLines& PreprocessorLines::operator=(const PreprocessorLines& other) {
    if (this != &other) {
        lines_ = other.lines_;
    }
    return *this;   
}

void PreprocessorLines::addLine(const PreprocessorLine& line) {
    lines_.emplace_back(line);
}

PreprocessorLines::iterator PreprocessorLines::begin() const {
    return lines_.begin();
}

PreprocessorLines::iterator PreprocessorLines::end() const {
    return lines_.end();
}

PreprocessorLine PreprocessorLines::getEOFAsPreprocessorLine() const {
    return lines_.rbegin()->atEOF();
}

PreprocessorLines PreprocessorLines::preprocess(const lexer::file_reader::FileLines& lines) {
    PreprocessorLines lineTokens;
    for (auto line : lines) {
        PreprocessorLine currentLineTokens(line);
        lineTokens.addLine(currentLineTokens);
    }
    return lineTokens;
}

void PreprocessorLines::print() const {

    // Print the tokens per line
    for (const PreprocessorLine& line : lines_) {
        if (line.empty()) {
            continue;
        }
        std::cout
            << "=============================================" << std::endl
            << "\"" << line.getLineWithoutWhitespace() << "\"" << std::endl
            << "FileLine " << line.getFileLine().getFileLocation().toString()
            << " Leading Whitespace: " << line.getLeadingWhitespace().size()
            << " Tokens: " << std::endl;
        // #PreprocessorTokenTypeNamesNeedToBeKeptInSync
        for (const PreprocessorToken& token : line.getTokens()) {
            switch (token.type) {
                case PreprocessorTokenType::QUOTED_STRING:
                    std::cout << "  QUOTED_STRING: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::ESCAPED_CHARACTER:
                    std::cout << "  ESCAPED_CHARACTER: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::MULTI_LINE_STRING:
                    std::cout << "  MULTI_LINE_STRING: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::COLON:
                    std::cout << "  COLON: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::OPEN_PARENTHESIS:
                    std::cout << "  OPEN_PARENTHESIS: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::CLOSE_PARENTHESIS:
                    std::cout << "  CLOSE_PARENTHESIS: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::OPEN_BRACKET:
                    std::cout << "  OPEN_BRACKET: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::CLOSE_BRACKET:
                    std::cout << "  CLOSE_BRACKET: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::OPEN_CURLY_BRACE:
                    std::cout << "  OPEN_CURLY_BRACE: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::CLOSE_CURLY_BRACE:
                    std::cout << "  CLOSE_CURLY_BRACE: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::COMMA:
                    std::cout << "  COMMA: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::MINUS_MINUS:
                    std::cout << "  MINUS_MINUS: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::MINUS_MINUS_MINUS:
                    std::cout << "  MINUS_MINUS_MINUS: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::NORMAL:
                    std::cout << "  NORMAL: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::COMMENT_OR_STRING_CONTENT:
                    std::cout << "  COMMENT_OR_STRING_CONTENT: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::BEGIN_SINGLE_LINE_STRING:
                    std::cout << "  BEGIN_SINGLE_LINE_STRING: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::END_SINGLE_LINE_STRING:
                    std::cout << "  END_SINGLE_LINE_STRING: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::BEGIN_MULTI_LINE_STRING:
                    std::cout << "  BEGIN_MULTI_LINE_STRING: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::END_MULTI_LINE_STRING:
                    std::cout << "  END_MULTI_LINE_STRING: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::BEGIN_BLOCK:
                    std::cout << "  BEGIN_BLOCK: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::END_BLOCK:
                    std::cout << "  END_BLOCK: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::BEGIN_SINGLE_LINE_COMMENT:
                    std::cout << "  BEGIN_SINGLE_LINE_COMMENT: " << token.text << std::endl;
                    break;
                case PreprocessorTokenType::END_SINGLE_LINE_COMMENT:
                    std::cout << "  END_SINGLE_LINE_COMMENT: " << token.text << std::endl;
                    break;
                default:
                    throw Exception("oops");
            }
        }
    }
}

} // namespace preprocessor
} // namespace lexer
} // namespace yapllang
} // namespace org
