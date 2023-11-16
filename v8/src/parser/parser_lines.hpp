#pragma once
#ifndef ORG_YAPLLANG_PARSER_LINES_HPP
#define ORG_YAPLLANG_PARSER_LINES_HPP

#include "include.hpp"
#include "parser/parser_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace tokenizer {
    class TokenizerLines;
}
}
namespace parser {

class ParserLines {
public:
    ParserLines();
    ParserLines(const ParserLines& other);
    ParserLines& operator=(const ParserLines& other);

    void addLine(const ParserLine& line);
    using iterator = std::vector<ParserLine>::const_iterator;
    iterator begin() const;
    iterator end() const;

    void print() const;
    static ParserLines parse(const lexer::tokenizer::TokenizerLines& lines);

private:
    std::vector<ParserLine> lines_;
};

} // namespace parser
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PARSER_LINES_HPP
