#pragma once
#ifndef ORG_YAPLLANG_PARSER_STATES_HPP
#define ORG_YAPLLANG_PARSER_STATES_HPP

#include "include.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace parser {
namespace states {

// #ParserStateMustStayInSync
enum class ParserState {
    HANDLING_BEGIN_FILE,
    HANDLING_NORMAL_STUFF,
    HANDLING_SINGLE_LINE_COMMENT,
    HANDLING_QUOTED_STRING,
    HANDLING_MULTI_LINE_STRING,
    STARTING_INDENTED_BLOCK,
    HANDLING_INDENTED_BLOCK,
    HANDLING_PARENTHESIS,
    HANDLING_BRACKETS,
    HANDLING_CURLY_BRACES
};

std::string to_string(const ParserState state);

} // namespace states
} // namespace parser
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PARSER_STATES_HPP
