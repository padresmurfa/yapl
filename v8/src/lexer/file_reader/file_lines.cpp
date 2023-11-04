#include "file_lines.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

FileLines::FileLines() {
}

FileLines::FileLines(const FileLines& other)
    : lines_(other.lines_)
{
}

FileLines& FileLines::operator=(const FileLines& other) {
    if (this != &other) {
        lines_ = other.lines_;
    }
    return *this;
}

void FileLines::addLine(const FileLine& line) {
    lines_.emplace_back(line);
}

FileLines::iterator FileLines::begin() const {
    return lines_.begin();
}

FileLines::iterator FileLines::end() const {
    return lines_.end();
}

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org
