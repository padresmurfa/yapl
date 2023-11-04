#pragma once
#ifndef ORG_YAPLLANG_TOOLS_STACKTRACE_HPP
#define ORG_YAPLLANG_TOOLS_STACKTRACE_HPP

#include <fstream>
#include <string>
#include <vector>
#include <stdexcept>
#include <iostream>
#include <regex>
#include <sstream>
#include <iomanip>
#include <locale>
#include <codecvt>
#include <execinfo.h>
#include <cxxabi.h>

namespace org {
namespace yapllang {
namespace tools {

struct StackFrame {
    size_t depth;
    std::string binary;
    std::string address;
    std::string symbol;
    std::string demangledSymbol;

    friend std::ostream& operator<<(std::ostream& os, const StackFrame& obj);
};

class StackTrace {
    public:
        StackTrace();
        StackTrace(const StackTrace& other);
        StackTrace& operator=(const StackTrace& other);

    public:
        static StackTrace capture();
        friend std::ostream& operator<<(std::ostream& os, const StackTrace& obj);
    private:
        std::vector<StackFrame> stackFrames_;
};

} // namespace tools
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_TOOLS_STACKTRACE_HPP
