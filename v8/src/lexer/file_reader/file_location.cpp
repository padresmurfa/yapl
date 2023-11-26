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

FileLocation::FileLocation(size_t lineNumber, size_t fileOffset, size_t lineOffsetInBytes)
    : lineNumber_(lineNumber)
    , fileOffset_(fileOffset)
    , lineOffsetInBytes_(lineOffsetInBytes)
{
}

// Copy constructor
FileLocation::FileLocation(const FileLocation& other)
    : lineNumber_(other.lineNumber_)
    , fileOffset_(other.fileOffset_)
    , lineOffsetInBytes_(other.lineOffsetInBytes_)
{
}

// Copy assignment operator
FileLocation& FileLocation::operator=(const FileLocation& other) {
    if (this != &other) {
        lineNumber_ = other.lineNumber_;
        fileOffset_ = other.fileOffset_;
        lineOffsetInBytes_ = other.lineOffsetInBytes_;
    }
    return *this;
}

bool FileLocation::operator==(const FileLocation& other) const {
    return lineNumber_ == other.lineNumber_
        && fileOffset_ == other.fileOffset_
        && lineOffsetInBytes_ == other.lineOffsetInBytes_;
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
    return FileLocation(lineNumber_, fileOffset_ + lineOffsetInBytes, lineOffsetInBytes_ + lineOffsetInBytes);
}

FileLocation FileLocation::offsetByBytes(size_t offsetInBytes) const {
    return FileLocation(lineNumber_, fileOffset_ + offsetInBytes, lineOffsetInBytes_ + offsetInBytes);
}

std::string FileLocation::toString() const {
    return "FileLocation(fileOffset='" + std::to_string(fileOffset_) + " (bytes)'" 
        + ", lineNumber='" + std::to_string(lineNumber_) + "'"
        + ", lineOffset='" + std::to_string(lineOffsetInBytes_) + " (bytes)')" 
        ;
}

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org
