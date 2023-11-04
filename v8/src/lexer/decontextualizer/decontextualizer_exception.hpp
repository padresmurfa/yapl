#pragma once

#ifndef ORG_YAPLLANG_LEXER_DECONTEXTUALIZER_EXCEPTION_HPP
#define ORG_YAPLLANG_LEXER_DECONTEXTUALIZER_EXCEPTION_HPP
 
#include "../lexer_exception.hpp"
#include "lexer/preprocessor/preprocessor.hpp"
#include "states/decontextualizer_states.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {

class DecontextualizerException : public LexerException {
public:
    DecontextualizerException(const std::string& message);
    DecontextualizerException(const DecontextualizerException& other);
    DecontextualizerException& operator=(const DecontextualizerException& other);
};

class ClosingUnopenedBlockException : public DecontextualizerException {
public:
    ClosingUnopenedBlockException(const preprocessor::PreprocessorToken& token);
    ClosingUnopenedBlockException(const ClosingUnopenedBlockException& other);
    ClosingUnopenedBlockException& operator=(const ClosingUnopenedBlockException& other);

private:
    preprocessor::PreprocessorToken token_;
};

class UnknownEscapeCharacterException : public DecontextualizerException {
public:
    UnknownEscapeCharacterException(const preprocessor::PreprocessorToken& token);
    UnknownEscapeCharacterException(const UnknownEscapeCharacterException& other);
    UnknownEscapeCharacterException& operator=(const UnknownEscapeCharacterException& other);
private:
    preprocessor::PreprocessorToken token_;
};

class InvalidTokenInThisContextException : public DecontextualizerException {
public:
    InvalidTokenInThisContextException(const preprocessor::PreprocessorToken& token, const states::DecontextualizerState state, const std::string &message);
    InvalidTokenInThisContextException(const InvalidTokenInThisContextException& other);
    InvalidTokenInThisContextException& operator=(const InvalidTokenInThisContextException& other);
private:
    preprocessor::PreprocessorToken token_;
    states::DecontextualizerState state_;
};

class UnclosedOpenedBlockException : public DecontextualizerException {
public:
    UnclosedOpenedBlockException(const std::string &message);
    UnclosedOpenedBlockException(const UnclosedOpenedBlockException& other);
    UnclosedOpenedBlockException& operator=(const UnclosedOpenedBlockException& other);
};


} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_LEXER_DECONTEXTUALIZER_EXCEPTION_HPP
