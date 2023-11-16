#include "parser_exception.hpp"
 
namespace org {
namespace yapllang {
namespace lexer {
namespace parser {

ParserException::ParserException(const std::string& message) : Exception(message)
{
}

ParserException::ParserException(const ParserException& other)
    : Exception(other)
{
}

ParserException& ParserException::operator=(const ParserException& other) {
    return *this;
}

ClosingUnopenedBlockException::ClosingUnopenedBlockException(const tokenizer::TokenizerToken& token)
    : ParserException("Closing Unopened Block: " + token.toString())
    , token_(token)
{   
}

ClosingUnopenedBlockException::ClosingUnopenedBlockException(const ClosingUnopenedBlockException& other)
    : ParserException(other)
    , token_(other.token_)
{
}

ClosingUnopenedBlockException& ClosingUnopenedBlockException::operator=(const ClosingUnopenedBlockException& other) {
    if (this == &other) {
        return *this; // Self-assignment, no action needed
    }
    
    // Call the base class's copy assignment operator
    ParserException::operator=(other);
    token_ = other.token_;

    return *this;
}


UnknownEscapeCharacterException::UnknownEscapeCharacterException(const tokenizer::TokenizerToken& token)
    : ParserException("Unknown Escape Character: '" + token.toString() + "'")
    , token_(token)
{   
}

UnknownEscapeCharacterException::UnknownEscapeCharacterException(const UnknownEscapeCharacterException& other)
    : ParserException(other)
    , token_(other.token_)
{
}

UnknownEscapeCharacterException& UnknownEscapeCharacterException::operator=(const UnknownEscapeCharacterException& other) {
    if (this == &other) {
        return *this; // Self-assignment, no action needed
    }
    
    // Call the base class's copy assignment operator
    ParserException::operator=(other);
    token_ = other.token_;

    return *this;
}


InvalidTokenInThisContextException::InvalidTokenInThisContextException(const tokenizer::TokenizerToken& token, const states::ParserState state, const std::string &message)
    : ParserException("Invalid Token in this context: '" + token.toString() + "', state=" + to_string(state))
    , token_(token)
    , state_(state)
{   
}

InvalidTokenInThisContextException::InvalidTokenInThisContextException(const InvalidTokenInThisContextException& other)
    : ParserException(other)
    , token_(other.token_)
    , state_(other.state_)
{
}

InvalidTokenInThisContextException& InvalidTokenInThisContextException::operator=(const InvalidTokenInThisContextException& other) {
    if (this == &other) {
        return *this; // Self-assignment, no action needed
    }
    
    // Call the base class's copy assignment operator
    ParserException::operator=(other);
    token_ = other.token_;
    state_ = other.state_;

    return *this;
}

UnclosedOpenedBlockException::UnclosedOpenedBlockException(const std::string &message)
    : ParserException(message)
{   
}

UnclosedOpenedBlockException::UnclosedOpenedBlockException(const UnclosedOpenedBlockException& other)
    : ParserException(other)
{
}

UnclosedOpenedBlockException& UnclosedOpenedBlockException::operator=(const UnclosedOpenedBlockException& other) {
    if (this == &other) {
        return *this; // Self-assignment, no action needed
    }
    
    // Call the base class's copy assignment operator
    ParserException::operator=(other);
 
    return *this;
}


} // namespace parser
} // namespace lexer
} // namespace yapllang
} // namespace org
