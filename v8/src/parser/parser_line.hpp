#pragma once
#ifndef ORG_YAPLLANG_PARSER_LINE_HPP
#define ORG_YAPLLANG_PARSER_LINE_HPP

#include "states/parser_context.hpp"
#include "lexer/tokenizer/tokenizer.hpp"
#include "lexer/tokenizer/tokenizer_line.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace parser {

using namespace org::yapllang;

class ParserLine {
public:
    ParserLine();
    ParserLine(const tokenizer::TokenizerLine& line, const std::vector<tokenizer::TokenizerToken> &tokens);
    ParserLine(const ParserLine& other);
    ParserLine& operator=(const ParserLine& other);

    bool empty() const;
    const lexer::tokenizer::TokenizerLine& getTokenizerLine() const;
    const lexer::file_reader::FileLocation& getFileLocation() const;
    const std::vector<tokenizer::TokenizerToken>& getTokens() const;

    std::string toString() const;

private:
    lexer::tokenizer::TokenizerLine tokenizerLine_;
    std::vector<tokenizer::TokenizerToken> tokens_;
};

} // namespace parser
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PARSER_LINE_HPP
