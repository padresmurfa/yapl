#pragma once
#ifndef ORG_YAPLLANG_DECONTEXTUALIZER_LINE_HPP
#define ORG_YAPLLANG_DECONTEXTUALIZER_LINE_HPP

#include "states/decontextualizer_context.hpp"
#include "lexer/preprocessor/preprocessor.hpp"
#include "lexer/preprocessor/preprocessor_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {

using namespace org::yapllang;

class DecontextualizerLine {
public:
    DecontextualizerLine();
    DecontextualizerLine(const preprocessor::PreprocessorLine& line, const std::vector<preprocessor::PreprocessorToken> &tokens);
    DecontextualizerLine(const DecontextualizerLine& other);
    DecontextualizerLine& operator=(const DecontextualizerLine& other);

    bool empty() const;
    const lexer::preprocessor::PreprocessorLine& getPreprocessorLine() const;
    const lexer::file_reader::FileLocation& getFileLocation() const;
    const std::vector<preprocessor::PreprocessorToken>& getTokens() const;

    std::string toString() const;

private:
    lexer::preprocessor::PreprocessorLine preprocessorLine_;
    std::vector<preprocessor::PreprocessorToken> tokens_;
};

} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_DECONTEXTUALIZER_LINE_HPP
