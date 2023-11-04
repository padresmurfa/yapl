#pragma once
#ifndef ORG_YAPLLANG_LEXER_LEXEREXCEPTION_HPP
#define ORG_YAPLLANG_LEXER_LEXEREXCEPTION_HPP

#include "include.hpp"
#include "tools/exception.hpp"

namespace org {
namespace yapllang {
namespace lexer {

class LexerException : public tools::Exception {
public:
    LexerException(const std::string& message);
    LexerException(const LexerException& other);
    LexerException& operator=(const LexerException& other);
};

} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_LEXER_LEXEREXCEPTION_HPP
