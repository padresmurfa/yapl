#include "stacktrace.hpp"

namespace org {
namespace yapllang {
namespace tools {

const size_t BACKTRACE_BUFFER_SIZE = 1000;

StackTrace::StackTrace()
{
    
}

StackTrace::StackTrace(const StackTrace& other)
    : stackFrames_(other.stackFrames_)
{
}

StackTrace& StackTrace::operator=(const StackTrace& other) {
    if (this == &other) {
        return *this; // Self-assignment, no action needed
    }
    stackFrames_ = other.stackFrames_;
    return *this;
}

std::string demangleSymbol(const std::string &symbol) {
    std::string result = symbol;
    // C++ name-mangled strings always starts with _Z (https://en.wikipedia.org/wiki/Name_mangling#Name_mangling_in_C.2B.2B)
    if (symbol.substr(0,2) == "_Z") {
        int status = -1;
        // using demangle from cxxabi.h
        char *demangledName = abi::__cxa_demangle( symbol.c_str(), NULL, NULL, &status );
        try {
            if ( status == 0 )
            {
                result = std::string(demangledName);
            }
        } catch(...) {
            free( demangledName );
            throw;
        }
        free( demangledName );
    }
    return result;
}

StackTrace StackTrace::capture() {
    StackTrace result;
    void **buffer = (void**)malloc(BACKTRACE_BUFFER_SIZE);
    try {
        // using backtrace from execinfo.h
        int returned = backtrace(buffer, BACKTRACE_BUFFER_SIZE);
        char **symbols = backtrace_symbols(buffer, BACKTRACE_BUFFER_SIZE);
        try {
            // skip stack frame 0, which is this function (captureStackTrace)
            for (size_t stackFrameDepth=1; stackFrameDepth<returned; stackFrameDepth++) {
                std::istringstream iss(symbols[stackFrameDepth]);
                std::vector<std::string> tokens;
                std::string token;
                while (iss >> token) {
                    tokens.push_back(token);
                }
                const std::string &symbol = tokens[3];
                const std::string demangledSymbol = demangleSymbol(symbol);
                StackFrame frame({
                    .depth = stackFrameDepth,
                    .binary = tokens[1],
                    .address = tokens[2],
                    .symbol = symbol,
                    .demangledSymbol = demangledSymbol
                });
                result.stackFrames_.push_back(frame);
            }
        } catch (...) {
            free(symbols);
            throw;
        }
        free(symbols);
    } catch (...) {
        free(buffer);
        throw;
    }
    free(buffer);
    return result;
}

std::ostream& operator<<(std::ostream& os, const StackFrame& obj) {
    static auto ignoreSymbols = {
        "_ZN3org8yapllang5tools9ExceptionC2ERKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEE",
        "_ZN3org8yapllang5lexer14LexerExceptionC2ERKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEE",
        "_ZN3org8yapllang5lexer16parser25ParserExceptionC2ERKNSt3__112basic_stringIcNS4_11char_traitsIcEENS4_9allocatorIcEEEE",
        "_ZN3org8yapllang5lexer16parser34InvalidTokenInThisContextExceptionC2ERKNS1_12tokenizeor17PreprocessorTokenENS2_6states21ParserStateERKNSt3__112basic_stringIcNSA_11char_traitsIcEENSA_9allocatorIcEEEE",
        "_ZN3org8yapllang5lexer16parser34InvalidTokenInThisContextExceptionC1ERKNS1_12tokenizeor17PreprocessorTokenENS2_6states21ParserStateERKNSt3__112basic_stringIcNSA_11char_traitsIcEENSA_9allocatorIcEEEE",
        "_ZN3org8yapllang5tools9ExceptionC1ERKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEE",
        "_ZN3org8yapllang5lexer16parser6states23ParserContext9exceptionERKNSt3__112basic_stringIcNS5_11char_traitsIcEENS5_9allocatorIcEEEE"
    };
    for (auto i : ignoreSymbols) {
        if (i == obj.symbol) {
            return os;
        }
    }
    static auto ignoreBinaries = {
        "dyld"
    };
    for (auto i : ignoreBinaries) {
        if (i == obj.binary) {
            return os;
        }
    }
    os << "  --------------------------------------------------------------------------------------------------------" << std::endl;
    os << "  " << obj.depth << ": StackFrame: " << std::endl;
    // os << "    depth: " << obj.depth << std::endl;
    os << "    binary: " << obj.binary << std::endl;
    os << "    address: " << obj.address << std::endl;
    os << "    demangledSymbol: " << obj.demangledSymbol << std::endl;
    if (obj.symbol != obj.demangledSymbol) {
        os << "    symbol: " << obj.symbol << std::endl;
    }
    return os;
}

std::ostream& operator<<(std::ostream& os, const StackTrace& obj) {
    // Define the output format for MyClass
    os << "StackTrace: " << std::endl;
    for (auto frame : obj.stackFrames_) {
        os << frame;
    }
    return os;
}

} // namespace tools
} // namespace yapllang
} // namespace org
