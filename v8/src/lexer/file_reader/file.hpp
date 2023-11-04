#pragma once

#ifndef ORG_YAPLLANG_LEXER_FILE_HPP
#define ORG_YAPLLANG_LEXER_FILE_HPP

#include "include.hpp"
#include "file_lines.hpp"
#include "file_reader_exception.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

class File {
public:
    File(const std::string& filename);
    File(const File& other);
    File& operator=(const File& other);

    void readLines();
    const FileLines& getLines() const;
    const std::string& getFilename() const;

private:
    std::string filename_;
    FileLines lines_;
};

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_LEXER_FILE_HPP
