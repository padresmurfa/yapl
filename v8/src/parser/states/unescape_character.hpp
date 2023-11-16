#pragma once
#ifndef ORG_YAPLLANG_PARSER_STATES_UNESCAPE_CHARACTER_HPP
#define ORG_YAPLLANG_PARSER_STATES_UNESCAPE_CHARACTER_HPP

#include "include.hpp"

namespace org {
namespace yapllang {
namespace parser {
class ParserToken;
namespace states {

std::string unescapeCharacter(const std::string &escapedCharacter, const parser::ParserToken &token);

} // namespace states
} // namespace parser
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PARSER_STATES_UNESCAPE_CHARACTER_HPP
