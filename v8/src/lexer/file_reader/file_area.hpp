#pragma once

#ifndef ORG_YAPLLANG_LEXER_FILE_AREA_HPP
#define ORG_YAPLLANG_LEXER_FILE_AREA_HPP

#include "include.hpp"
#include "file_location.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

class FileArea {
public:
    FileArea();
    FileArea(const std::string& filename, const FileLocation& begin, const FileLocation& end);
    FileArea(const FileArea& other);
    FileArea& operator=(const FileArea& other);
    bool operator==(const FileArea& other) const;

    const std::string& getFilename() const;

    const FileLocation &getBegin() const;
    const FileLocation &getEnd() const;

    std::string toString() const;

private:
    std::string filename_;
    FileLocation begin_;
    FileLocation end_;
};

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_LEXER_FILE_AREA_HPP
