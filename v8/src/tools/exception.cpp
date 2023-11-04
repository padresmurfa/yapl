#include "exception.hpp"

namespace org {
namespace yapllang {
namespace tools {

Exception::Exception(const std::string& message)
    : std::runtime_error(message)
{
    stackTrace_ = StackTrace::capture();
}

Exception::Exception(const Exception& other)
    : std::runtime_error(other)
    , stackTrace_(other.stackTrace_)
{
}

Exception& Exception::operator=(const Exception& other) {
    if (this == &other) {
        return *this; // Self-assignment, no action needed
    }
    std::runtime_error::operator=(other);
    stackTrace_ = other.stackTrace_;
    return *this;
}

const StackTrace &Exception::getStackTrace() const {
    return stackTrace_;
}

} // namespace tools
} // namespace yapllang
} // namespace org
