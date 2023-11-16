#pragma once
#ifndef ORG_YAPLLANG_PARSER_LINE_HPP
#define ORG_YAPLLANG_PARSER_LINE_HPP

#include "states/parser_context.hpp"
#include "lexer/tokenizer/tokenizer.hpp"
#include "lexer/tokenizer/tokenizer_line.hpp"

namespace org {
namespace yapllang {
namespace parser {

using namespace org::yapllang;

class ParserLine {
public:
    ParserLine();
    ParserLine(const lexer::tokenizer::TokenizerLine& line, const std::vector<ParserToken> &tokens);
    ParserLine(const ParserLine& other);
    ParserLine& operator=(const ParserLine& other);

    bool empty() const;
    const lexer::tokenizer::TokenizerLine& getTokenizerLine() const;
    const lexer::file_reader::FileLocation& getFileLocation() const;
    const std::vector<ParserToken>& getTokens() const;

    std::string toString() const;

private:
    lexer::tokenizer::TokenizerLine tokenizerLine_;
    std::vector<ParserToken> tokens_;
};

} // namespace parser
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PARSER_LINE_HPP
