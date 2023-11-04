#include "file_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

FileLine::FileLine() {}

FileLine::FileLine(const std::string& text, const FileLocation& fileLocation)
    : text_(text), fileLocation_(fileLocation) {}

FileLine::FileLine(const FileLine& other)
    : text_(other.text_)
    , fileLocation_(other.fileLocation_)
{
}

FileLine& FileLine::operator=(const FileLine& other) {
    if (this != &other) {
        text_ = other.text_;
        fileLocation_ = other.fileLocation_;
    }
    return *this;
}

const std::string& FileLine::getText() const {
    return text_;
}

const FileLocation& FileLine::getFileLocation() const {
    return fileLocation_;
}

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org
