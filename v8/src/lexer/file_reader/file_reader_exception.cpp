#include "file_reader_exception.hpp"
 
namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

FileReaderException::FileReaderException(const std::string& message)
    : LexerException(message)
{
}

FileReaderException::FileReaderException(const FileReaderException& other)
    : LexerException(other)
{
}

FileReaderException& FileReaderException::operator=(const FileReaderException& other) {
    if (this == &other) {
        return *this;
    }
    LexerException::operator=(other);

    return *this;
}

FileOpenFailedException::FileOpenFailedException(const std::string& message)
    : FileReaderException(message)
{
}

FileOpenFailedException::FileOpenFailedException(const FileOpenFailedException& other)
    : FileReaderException(other)
{
}

FileOpenFailedException& FileOpenFailedException::operator=(const FileOpenFailedException& other) {
    if (this == &other) {
        return *this;
    }
    FileReaderException::operator=(other);

    return *this;
}

FileContainedInvalidUTF8Exception::FileContainedInvalidUTF8Exception(const FileLocation& fileLocation)
    : FileReaderException("Invalid UTF-8 byte (at " + fileLocation.toString())
    , fileLocation_(fileLocation)
{   
}

FileContainedInvalidUTF8Exception::FileContainedInvalidUTF8Exception(const FileContainedInvalidUTF8Exception& other)
    : FileReaderException(other)
    , fileLocation_(other.fileLocation_)
{
}

FileContainedInvalidUTF8Exception& FileContainedInvalidUTF8Exception::operator=(const FileContainedInvalidUTF8Exception& other) {
    if (this == &other) {
        return *this;
    }
    FileReaderException::operator=(other);
    fileLocation_ = other.fileLocation_;

    return *this;
}

const FileLocation& FileContainedInvalidUTF8Exception::getFileLocation() const {
    return fileLocation_;
}

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org
