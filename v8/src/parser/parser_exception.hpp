#pragma once

#ifndef ORG_YAPLLANG_LEXER_PARSER_EXCEPTION_HPP
#define ORG_YAPLLANG_LEXER_PARSER_EXCEPTION_HPP
 
#include "tools/exception.hpp"
#include "lexer/tokenizer/tokenizer.hpp"
#include "states/parser_states.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace parser {

class ParserException : public Exception {
public:
    ParserException(const std::string& message);
    ParserException(const ParserException& other);
    ParserException& operator=(const ParserException& other);
};

class ClosingUnopenedBlockException : public ParserException {
public:
    ClosingUnopenedBlockException(const tokenizer::TokenizerToken& token);
    ClosingUnopenedBlockException(const ClosingUnopenedBlockException& other);
    ClosingUnopenedBlockException& operator=(const ClosingUnopenedBlockException& other);

private:
    tokenizer::TokenizerToken token_;
};

class UnknownEscapeCharacterException : public ParserException {
public:
    UnknownEscapeCharacterException(const tokenizer::TokenizerToken& token);
    UnknownEscapeCharacterException(const UnknownEscapeCharacterException& other);
    UnknownEscapeCharacterException& operator=(const UnknownEscapeCharacterException& other);
private:
    tokenizer::TokenizerToken token_;
};

class InvalidTokenInThisContextException : public ParserException {
public:
    InvalidTokenInThisContextException(const tokenizer::TokenizerToken& token, const states::ParserState state, const std::string &message);
    InvalidTokenInThisContextException(const InvalidTokenInThisContextException& other);
    InvalidTokenInThisContextException& operator=(const InvalidTokenInThisContextException& other);
private:
    tokenizer::TokenizerToken token_;
    states::ParserState state_;
};

class UnclosedOpenedBlockException : public ParserException {
public:
    UnclosedOpenedBlockException(const std::string &message);
    UnclosedOpenedBlockException(const UnclosedOpenedBlockException& other);
    UnclosedOpenedBlockException& operator=(const UnclosedOpenedBlockException& other);
};


} // namespace parser
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_LEXER_PARSER_EXCEPTION_HPP
