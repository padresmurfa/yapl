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
        std::cout
            << "=============================================" << std::endl
            << "\"" << line.getLineWithoutWhitespace() << "\"" << std::endl
            << "FileArea " << line.getFileLine().getFileArea().toString() << std::endl
            << " Leading Whitespace: " << line.getLeadingWhitespace().size() << std::endl
            << " Tokens: " << std::endl;
        // #TokenizerTokenTypeNamesNeedToBeKeptInSync
        for (const TokenizerToken& token : line.getTokens()) {
            std::cout << std::endl << token.toString() << std::endl;
        }
    }
}

} // namespace tokenizer
} // namespace lexer
} // namespace yapllang
} // namespace org
