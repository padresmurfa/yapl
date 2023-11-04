#pragma once
#ifndef ORG_YAPLLANG_LEXER_LINES_HPP
#define ORG_YAPLLANG_LEXER_LINES_HPP

#include "include.hpp"
#include "file_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

class FileLines {
public:
    FileLines();
    FileLines(const FileLines& other);
    FileLines& operator=(const FileLines& other);

    void addLine(const FileLine& line);
    using iterator = std::vector<FileLine>::const_iterator;
    iterator begin() const;
    iterator end() const;

private:
    std::vector<FileLine> lines_;
};

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_LEXER_LINES_HPP
