#pragma once
#ifndef ORG_YAPLLANG_PREPROCESSOR_LINES_HPP
#define ORG_YAPLLANG_PREPROCESSOR_LINES_HPP

#include "include.hpp"
#include "preprocessor_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {
    class FileLines;
}
namespace preprocessor {

class PreprocessorLines {
public:
    PreprocessorLines();
    PreprocessorLines(const PreprocessorLines& other);
    PreprocessorLines& operator=(const PreprocessorLines& other);

    void addLine(const PreprocessorLine& line);
    using iterator = std::vector<PreprocessorLine>::const_iterator;
    iterator begin() const;
    iterator end() const;
    PreprocessorLine getEOFAsPreprocessorLine() const;

    void print() const;
    static PreprocessorLines preprocess(const lexer::file_reader::FileLines& lines);

private:
    std::vector<PreprocessorLine> lines_;

};

} // namespace preprocessor
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PREPROCESSOR_LINES_HPP
