#include "lexer_exception.hpp"

namespace org {
namespace yapllang {
namespace lexer {

LexerException::LexerException(const std::string& message)
    : tools::Exception(message)
{
    
}

LexerException::LexerException(const LexerException& other)
    : tools::Exception(other)
{
}

LexerException& LexerException::operator=(const LexerException& other) {
    if (this == &other) {
        return *this; // Self-assignment, no action needed
    }
    tools::Exception::operator=(other);
    return *this;
}

} // namespace lexer
} // namespace yapllang
} // namespace org
