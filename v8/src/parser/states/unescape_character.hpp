#pragma once
#ifndef ORG_YAPLLANG_PARSER_STATES_UNESCAPE_CHARACTER_HPP
#define ORG_YAPLLANG_PARSER_STATES_UNESCAPE_CHARACTER_HPP

#include "include.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace tokenizer {
    class TokenizerToken;
}
namespace parser {
namespace states {

std::string unescapeCharacter(const std::string &escapedCharacter, const lexer::tokenizer::TokenizerToken &token);

} // namespace states
} // namespace parser
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PARSER_STATES_UNESCAPE_CHARACTER_HPP
