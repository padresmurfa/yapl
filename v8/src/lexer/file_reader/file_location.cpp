#include "file_location.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

FileLocation::FileLocation()
    : lineNumber_(0)
    , fileOffset_(0)
    , lineOffsetInBytes_(0)
{
}

FileLocation::FileLocation(const std::string& filename, size_t lineNumber, size_t fileOffset, size_t lineOffsetInBytes)
    : filename_(filename)
    , lineNumber_(lineNumber)
    , fileOffset_(fileOffset)
    , lineOffsetInBytes_(lineOffsetInBytes)
{
}

// Copy constructor
FileLocation::FileLocation(const FileLocation& other)
    : filename_(other.filename_)
    , lineNumber_(other.lineNumber_)
    , fileOffset_(other.fileOffset_)
    , lineOffsetInBytes_(other.lineOffsetInBytes_)
{
}

// Copy assignment operator
FileLocation& FileLocation::operator=(const FileLocation& other) {
    if (this != &other) {
        filename_ = other.filename_;
        lineNumber_ = other.lineNumber_;
        fileOffset_ = other.fileOffset_;
        lineOffsetInBytes_ = other.lineOffsetInBytes_;
    }
    return *this;
}

const std::string& FileLocation::getFilename() const {
    return filename_;
}

size_t FileLocation::getLineNumber() const {
    return lineNumber_;
}

size_t FileLocation::getFileOffset() const {
    return fileOffset_;
}

size_t FileLocation::getLineOffsetInBytes() const {
    return lineOffsetInBytes_;
}

FileLocation FileLocation::withLineOffsetInBytes(size_t lineOffsetInBytes) const {
    return FileLocation(filename_, lineNumber_, fileOffset_ + lineOffsetInBytes, lineOffsetInBytes_ + lineOffsetInBytes);
}

FileLocation FileLocation::offsetByBytes(size_t offsetInBytes) const {
    return FileLocation(filename_, lineNumber_, fileOffset_ + offsetInBytes, lineOffsetInBytes_ + offsetInBytes);
}

std::string FileLocation::toString() const {
    return "File: " + filename_
        + ", File Offset: " + std::to_string(fileOffset_) + " (bytes)" 
        + ", Line Number: " + std::to_string(lineNumber_)
        + ", Line Offset: " + std::to_string(lineOffsetInBytes_) + " (bytes)" 
        ;
}

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org
