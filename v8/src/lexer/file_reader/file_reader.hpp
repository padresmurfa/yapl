#pragma once

#ifndef ORG_YAPLLANG_LEXER_FILE_READER_HPP
#define ORG_YAPLLANG_LEXER_FILE_READER_HPP

#include "include.hpp"
#include "file.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

class FileReader {
public:
    FileReader(const std::string& filename);
    FileReader(const FileReader& other);
    FileReader& operator=(const FileReader& other);

    const FileLines& getLines() const;
    const File& getFile() const;

    void print() const;

private:
    File file_;
};

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_LEXER_FILE_READER_HPP
