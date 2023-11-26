#pragma once

#ifndef ORG_YAPLLANG_LEXER_FILE_LOCATION_HPP
#define ORG_YAPLLANG_LEXER_FILE_LOCATION_HPP

#include "include.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

class FileLocation {
public:
    FileLocation();
    FileLocation(size_t lineNumber, size_t fileOffset, size_t lineOffsetInBytes);
    FileLocation(const FileLocation& other);
    FileLocation& operator=(const FileLocation& other);
    bool operator==(const FileLocation& other) const;

    size_t getLineNumber() const;
    size_t getFileOffset() const;
    size_t getLineOffsetInBytes() const;
    std::string toString() const;

    FileLocation withLineOffsetInBytes(size_t lineOffsetInBytes) const;
    FileLocation offsetByBytes(size_t offsetInBytes) const;

private:
    size_t lineNumber_;
    size_t fileOffset_;
    size_t lineOffsetInBytes_;
};

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_LEXER_FILE_LOCATION_HPP
