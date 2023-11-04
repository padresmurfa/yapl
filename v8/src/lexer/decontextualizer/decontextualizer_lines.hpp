#pragma once
#ifndef ORG_YAPLLANG_DECONTEXTUALIZER_LINES_HPP
#define ORG_YAPLLANG_DECONTEXTUALIZER_LINES_HPP

#include "include.hpp"
#include "lexer/decontextualizer/decontextualizer_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace preprocessor {
    class PreprocessorLines;
}
namespace decontextualizer {

class DecontextualizerLines {
public:
    DecontextualizerLines();
    DecontextualizerLines(const DecontextualizerLines& other);
    DecontextualizerLines& operator=(const DecontextualizerLines& other);

    void addLine(const DecontextualizerLine& line);
    using iterator = std::vector<DecontextualizerLine>::const_iterator;
    iterator begin() const;
    iterator end() const;

    void print() const;
    static DecontextualizerLines decontextualize(const lexer::preprocessor::PreprocessorLines& lines);

private:
    std::vector<DecontextualizerLine> lines_;
};

} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_DECONTEXTUALIZER_LINES_HPP
