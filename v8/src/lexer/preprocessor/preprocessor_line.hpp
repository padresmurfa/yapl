#pragma once
#ifndef ORG_YAPLLANG_PREPROCESSOR_LINE_HPP
#define ORG_YAPLLANG_PREPROCESSOR_LINE_HPP

#include "preprocessor.hpp"
#include "lexer/file_reader/file_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {

namespace preprocessor {

using namespace org::yapllang;

class PreprocessorLine {
public:
    PreprocessorLine();
    PreprocessorLine(const lexer::file_reader::FileLine& line);
    PreprocessorLine(const PreprocessorLine& other);
    PreprocessorLine& operator=(const PreprocessorLine& other);

    std::string toString() const;
    bool empty() const;
    const lexer::file_reader::FileLine& getFileLine() const;
    const lexer::file_reader::FileLocation& getFileLocation() const;
    const std::string& getLeadingWhitespace() const;
    const std::string& getTrailingWhitespace() const;
    const std::string& getLineWithoutWhitespace() const;
    const std::vector<PreprocessorToken>& getTokens() const;

    PreprocessorLine atEOF() const;

private:
    lexer::file_reader::FileLine line_;
    std::string leadingWhitespace_;
    std::string trailingWhitespace_;
    std::string lineWithoutWhitespace_;
    std::vector<PreprocessorToken> tokens_;

    void initializeText();
    void initializeTokens();    
};

} // namespace preprocessor
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PREPROCESSOR_LINE_HPP
