#pragma once
#ifndef ORG_YAPLLANG_TOKENIZER_LINES_HPP
#define ORG_YAPLLANG_TOKENIZER_LINES_HPP

#include "include.hpp"
#include "tokenizer_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {
    class FileLines;
}
namespace tokenizer {

class TokenizerLines {
public:
    TokenizerLines();
    TokenizerLines(const TokenizerLines& other);
    TokenizerLines& operator=(const TokenizerLines& other);

    void addLine(const TokenizerLine& line);
    using iterator = std::vector<TokenizerLine>::const_iterator;
    iterator begin() const;
    iterator end() const;
    TokenizerLine getEOFAsTokenizerLine() const;

    void print() const;
    static TokenizerLines tokenize(const lexer::file_reader::FileLines& lines);

private:
    std::vector<TokenizerLine> lines_;

};

} // namespace tokenizer
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_TOKENIZER_LINES_HPP
