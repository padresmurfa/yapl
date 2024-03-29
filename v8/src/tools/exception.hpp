#pragma once
#ifndef ORG_YAPLLANG_TOOLS_EXCEPTION_HPP
#define ORG_YAPLLANG_TOOLS_EXCEPTION_HPP

#include "stacktrace.hpp"

#define BEGIN_SECTION() try {
#define END_SECTION(x) } catch (std::exception &ex) { std::cerr << "@" << x << std::endl; throw; }

namespace org {
namespace yapllang {
namespace tools {

class Exception : public std::runtime_error {
public:
    Exception(const std::string& message);
    Exception(const Exception& other);
    Exception& operator=(const Exception& other);

    const StackTrace &getStackTrace() const;
private:
    StackTrace stackTrace_;
};

} // namespace tools
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_TOOLS_EXCEPTION_HPP
