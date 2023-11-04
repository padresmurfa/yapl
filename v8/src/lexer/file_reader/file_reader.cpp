#include "include.hpp"
#include "file_reader.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

FileReader::FileReader(const std::string& filename) : file_(File(filename))
{
    file_.readLines();
}

FileReader::FileReader(const FileReader& other)
    : file_(other.file_)
{
}

FileReader& FileReader::operator=(const FileReader& other) {
    if (this != &other) {
        file_ = other.file_;
    }
    return *this;
}

const FileLines& FileReader::getLines() const
{
    return file_.getLines();
}

const File& FileReader::getFile() const
{
    return file_;
}

void FileReader::print() const {
    const FileLines &fileLines = getLines();
    for (auto it = fileLines.begin(); it != fileLines.end(); ++it) {
        auto line = *it;
        auto fileLocation = line.getFileLocation();

        std::cout << "Original Line: " << line.getText() << std::endl;
        std::cout << "FileLocation: Line " << fileLocation.getLineNumber()
                    << " (File Offset " << fileLocation.getFileOffsetInBytes()
                    << " (bytes)) in " << fileLocation.getFilename() << std::endl;
    }
}

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org
