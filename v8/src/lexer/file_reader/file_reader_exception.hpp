#pragma once

#ifndef ORG_YAPLLANG_LEXER_FILE_EXCEPTION_HPP
#define ORG_YAPLLANG_LEXER_FILE_EXCEPTION_HPP
 
#include "../lexer_exception.hpp"
#include "file_location.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

class FileReaderException : public LexerException {
public:
    FileReaderException(const std::string& message);
    FileReaderException(const FileReaderException& other);
    FileReaderException& operator=(const FileReaderException& other);
};

class FileOpenFailedException : public FileReaderException {
public:
    FileOpenFailedException(const std::string& message);
    FileOpenFailedException(const FileOpenFailedException& other);
    FileOpenFailedException& operator=(const FileOpenFailedException& other);
};

class FileContainedInvalidUTF8Exception : public FileReaderException {
public:
    FileContainedInvalidUTF8Exception(const FileLocation& fileLocation);
    FileContainedInvalidUTF8Exception(const FileContainedInvalidUTF8Exception& other);
    FileContainedInvalidUTF8Exception& operator=(const FileContainedInvalidUTF8Exception& other);

    const FileLocation& getFileLocation() const;
private:
    FileLocation fileLocation_;
};

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_LEXER_FILE_EXCEPTION_HPP
