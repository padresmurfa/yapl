#pragma once
#ifndef ORG_YAPLLANG_TOKENIZER_LINE_HPP
#define ORG_YAPLLANG_TOKENIZER_LINE_HPP

#include "tokenizer.hpp"
#include "lexer/file_reader/file_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {

namespace tokenizer {

using namespace org::yapllang;

class TokenizerLine {
public:
    TokenizerLine();
    TokenizerLine(const lexer::file_reader::FileLine& line);
    TokenizerLine(const TokenizerLine& other);
    TokenizerLine& operator=(const TokenizerLine& other);

    std::string toString() const;
    bool empty() const;
    const lexer::file_reader::FileLine& getFileLine() const;
    const lexer::file_reader::FileLocation& getFileLocation() const;
    const std::string& getLeadingWhitespace() const;
    const std::string& getTrailingWhitespace() const;
    const std::string& getLineWithoutWhitespace() const;
    const std::vector<TokenizerToken>& getTokens() const;

    TokenizerLine atEOF() const;

private:
    lexer::file_reader::FileLine line_;
    std::string leadingWhitespace_;
    std::string trailingWhitespace_;
    std::string lineWithoutWhitespace_;
    std::vector<TokenizerToken> tokens_;

    void initializeText();
    void initializeTokens();    
};

} // namespace tokenizer
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_TOKENIZER_LINE_HPP
