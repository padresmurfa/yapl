#pragma once
#ifndef ORG_YAPLLANG_LEXER_LINE_HPP
#define ORG_YAPLLANG_LEXER_LINE_HPP

#include "include.hpp"
#include "file_location.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace file_reader {

class FileLine {
public:
    FileLine();
    FileLine(const std::string& text, const FileLocation& fileLocation);
    FileLine(const FileLine& other);
    FileLine& operator=(const FileLine& other);

    const std::string& getText() const;
    const FileLocation& getFileLocation() const;

private:
    std::string text_;
    FileLocation fileLocation_;
};

} // namespace file_reader
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_LEXER_LINE_HPP
