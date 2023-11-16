#pragma once

#ifndef ORG_YAPLLANG_LEXER_PARSER_EXCEPTION_HPP
#define ORG_YAPLLANG_LEXER_PARSER_EXCEPTION_HPP
 
#include "tools/exception.hpp"
#include "parser/parser.hpp"
#include "states/parser_states.hpp"

namespace org {
namespace yapllang {
namespace parser {

class ParserException : public Exception {
public:
    ParserException(const std::string& message);
    ParserException(const ParserException& other);
    ParserException& operator=(const ParserException& other);
};

class ClosingUnopenedBlockException : public ParserException {
public:
    ClosingUnopenedBlockException(const parser::ParserToken& token);
    ClosingUnopenedBlockException(const ClosingUnopenedBlockException& other);
    ClosingUnopenedBlockException& operator=(const ClosingUnopenedBlockException& other);

private:
    parser::ParserToken token_;
};

class UnknownEscapeCharacterException : public ParserException {
public:
    UnknownEscapeCharacterException(const parser::ParserToken& token);
    UnknownEscapeCharacterException(const UnknownEscapeCharacterException& other);
    UnknownEscapeCharacterException& operator=(const UnknownEscapeCharacterException& other);
private:
    parser::ParserToken token_;
};

class InvalidTokenInThisContextException : public ParserException {
public:
    InvalidTokenInThisContextException(const parser::ParserToken& token, const states::ParserState state, const std::string &message);
    InvalidTokenInThisContextException(const InvalidTokenInThisContextException& other);
    InvalidTokenInThisContextException& operator=(const InvalidTokenInThisContextException& other);
private:
    parser::ParserToken token_;
    states::ParserState state_;
};

class UnclosedOpenedBlockException : public ParserException {
public:
    UnclosedOpenedBlockException(const std::string &message);
    UnclosedOpenedBlockException(const UnclosedOpenedBlockException& other);
    UnclosedOpenedBlockException& operator=(const UnclosedOpenedBlockException& other);
};


} // namespace parser
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_LEXER_PARSER_EXCEPTION_HPP
