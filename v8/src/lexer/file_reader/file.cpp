#include "include.hpp"
#include "file.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

File::File(const std::string& filename) : filename_(filename) {}

File::File(const File& other)
    : filename_(other.filename_)
    , lines_(other.lines_)
{
}

File& File::operator=(const File& other) {
    if (this != &other) {
        filename_ = other.filename_;
        lines_ = other.lines_;
    }
    return *this;
}

void expandTabs(const std::string &input, std::string &output) {
    std::stringstream tmp;

    // Iterate through the input string
    for (char c : input) {
        if (c == '\t') {
            tmp << "    ";
        } else {
            tmp << c;
        }
    }
    output = tmp.str();
}

void File::readLines() {
    std::ifstream inputFile(filename_, std::ios::binary); // Open in binary mode

    if (!inputFile.is_open()) {
        throw FileOpenFailedException("Failed to open the file: " + filename_);
    }

    std::string lineText; // Use std::string for text (can be UTF-8 or ASCII)
    size_t lineNumber = 1;
    size_t fileOffset = 0;

    try {
        while (std::getline(inputFile, lineText)) {
            FileLocation fileLocation(filename_, lineNumber, fileOffset);

            // Validate UTF-8 encoding
            if (!utf8::is_valid(lineText.begin(), lineText.end())) {
                size_t invalidUtf8Offset = utf8::find_invalid(lineText);
                auto invalidUtf8Location = fileLocation.withLineOffsetInBytes(invalidUtf8Offset);
                throw FileContainedInvalidUTF8Exception(invalidUtf8Location);
            }

            std::string preprocessedLineText;
            expandTabs(lineText, preprocessedLineText);

            FileLine line(preprocessedLineText, fileLocation);

            // Add the line to the Lines collection
            lines_.addLine(line);

            // Calculate the offset for the next line
            fileOffset += preprocessedLineText.size() + 1; // +1 for the newline character
            lineNumber++;
        }
    } catch (const std::exception& e) {
        // If an error occurs while reading, catch and wrap it as a FileReaderException
        throw FileReaderException("Error reading the file: " + std::string(e.what()));
    }

    inputFile.close();
}

const FileLines& File::getLines() const {
    return lines_;
}

const std::string& File::getFilename() const {
    return filename_;
}

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org
