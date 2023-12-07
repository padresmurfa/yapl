#include "file_area.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

FileArea::FileArea()
{
}

FileArea::FileArea(const std::string& filename, const FileLocation& begin, const FileLocation& end)
    : filename_(filename)
    , begin_(begin)
    , end_(end)
{
}

// Copy constructor
FileArea::FileArea(const FileArea& other)
    : filename_(other.filename_)
    , begin_(other.begin_)
    , end_(other.end_)
{
}

// Copy assignment operator
FileArea& FileArea::operator=(const FileArea& other) {
    if (this != &other) {
        filename_ = other.filename_;
        begin_ = other.begin_;
        end_ = other.end_;
    }
    return *this;
}

bool FileArea::operator==(const FileArea& other) const {
    return filename_ == other.filename_ 
        && begin_ == other.begin_
        && end_ == other.end_;
}

bool FileArea::isImmediatePredecessorOf(const FileArea& other) const {
    if (filename_ != other.filename_) {
        throw std::runtime_error("predecessor checks are only valid within the same file");
    }
    return end_.getFileOffset() == other.begin_.getFileOffset();
}

bool FileArea::isPredecessorLineOf(const FileArea& other) const {
    if (filename_ != other.filename_) {
        throw std::runtime_error("predecessor checks are only valid within the same file");
    }
    if ((1 + begin_.getLineNumber()) != other.begin_.getLineNumber()) {
        return false;
    }
    if (begin_.getLineOffsetInBytes() != other.begin_.getLineOffsetInBytes()) {
        return false;
    }
    return true;
}

void FileArea::extendTo(const FileArea& other) {
    if (filename_ != other.filename_) {
        throw std::runtime_error("cannot extend file areas across multiple files");
    }
    end_ = other.end_;
}

FileArea FileArea::asEndOfArea() const {
    return FileArea(
        filename_,
        end_,
        end_
    );
}

const std::string& FileArea::getFilename() const {
    return filename_;
}

const FileLocation& FileArea::getBegin() const {
    return begin_;
}

const FileLocation& FileArea::getEnd() const {
    return end_;
}

std::string FileArea::toString() const {
    return "FileArea(filename='" + filename_ + "', begin=" + begin_.toString() + ", end=" + end_.toString() + ")";
}

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org
