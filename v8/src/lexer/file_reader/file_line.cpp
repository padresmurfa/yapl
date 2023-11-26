#include "file_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

FileLine::FileLine() {}

FileLine::FileLine(const std::string& text, const FileArea& fileArea)
    : text_(text), fileArea_(fileArea)
{

}

FileLine::FileLine(const FileLine& other)
    : text_(other.text_)
    , fileArea_(other.fileArea_)
{
}

FileLine& FileLine::operator=(const FileLine& other) {
    if (this != &other) {
        text_ = other.text_;
        fileArea_ = other.fileArea_;
    }
    return *this;
}

const std::string& FileLine::getText() const {
    return text_;
}

const FileArea FileLine::getFileArea() const {
    return fileArea_;
}

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org
