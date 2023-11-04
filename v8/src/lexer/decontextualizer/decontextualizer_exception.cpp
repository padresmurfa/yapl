#include "decontextualizer_exception.hpp"
 
namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {

DecontextualizerException::DecontextualizerException(const std::string& message) : LexerException(message)
{
}

DecontextualizerException::DecontextualizerException(const DecontextualizerException& other)
    : LexerException(other)
{
}

DecontextualizerException& DecontextualizerException::operator=(const DecontextualizerException& other) {
    return *this;
}

ClosingUnopenedBlockException::ClosingUnopenedBlockException(const preprocessor::PreprocessorToken& token)
    : DecontextualizerException("Closing Unopened Block: " + token.toString())
    , token_(token)
{   
}

ClosingUnopenedBlockException::ClosingUnopenedBlockException(const ClosingUnopenedBlockException& other)
    : DecontextualizerException(other)
    , token_(other.token_)
{
}

ClosingUnopenedBlockException& ClosingUnopenedBlockException::operator=(const ClosingUnopenedBlockException& other) {
    if (this == &other) {
        return *this; // Self-assignment, no action needed
    }
    
    // Call the base class's copy assignment operator
    DecontextualizerException::operator=(other);
    token_ = other.token_;

    return *this;
}


UnknownEscapeCharacterException::UnknownEscapeCharacterException(const preprocessor::PreprocessorToken& token)
    : DecontextualizerException("Unknown Escape Character: '" + token.toString() + "'")
    , token_(token)
{   
}

UnknownEscapeCharacterException::UnknownEscapeCharacterException(const UnknownEscapeCharacterException& other)
    : DecontextualizerException(other)
    , token_(other.token_)
{
}

UnknownEscapeCharacterException& UnknownEscapeCharacterException::operator=(const UnknownEscapeCharacterException& other) {
    if (this == &other) {
        return *this; // Self-assignment, no action needed
    }
    
    // Call the base class's copy assignment operator
    DecontextualizerException::operator=(other);
    token_ = other.token_;

    return *this;
}


InvalidTokenInThisContextException::InvalidTokenInThisContextException(const preprocessor::PreprocessorToken& token, const states::DecontextualizerState state, const std::string &message)
    : DecontextualizerException("Invalid Token in this context: '" + token.toString() + "', state=" + to_string(state))
    , token_(token)
    , state_(state)
{   
}

InvalidTokenInThisContextException::InvalidTokenInThisContextException(const InvalidTokenInThisContextException& other)
    : DecontextualizerException(other)
    , token_(other.token_)
    , state_(other.state_)
{
}

InvalidTokenInThisContextException& InvalidTokenInThisContextException::operator=(const InvalidTokenInThisContextException& other) {
    if (this == &other) {
        return *this; // Self-assignment, no action needed
    }
    
    // Call the base class's copy assignment operator
    DecontextualizerException::operator=(other);
    token_ = other.token_;
    state_ = other.state_;

    return *this;
}

UnclosedOpenedBlockException::UnclosedOpenedBlockException(const std::string &message)
    : DecontextualizerException(message)
{   
}

UnclosedOpenedBlockException::UnclosedOpenedBlockException(const UnclosedOpenedBlockException& other)
    : DecontextualizerException(other)
{
}

UnclosedOpenedBlockException& UnclosedOpenedBlockException::operator=(const UnclosedOpenedBlockException& other) {
    if (this == &other) {
        return *this; // Self-assignment, no action needed
    }
    
    // Call the base class's copy assignment operator
    DecontextualizerException::operator=(other);
 
    return *this;
}


} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org
