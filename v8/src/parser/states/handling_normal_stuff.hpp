#pragma once
#ifndef ORG_YAPLLANG_PARSER_STATES_HANDLING_NORMAL_STUFF_HPP
#define ORG_YAPLLANG_PARSER_STATES_HANDLING_NORMAL_STUFF_HPP

#include "include.hpp"
#include "parser_context.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace tokenizer {
    class TokenizerToken;
}
namespace parser {
namespace states {

void handlingNormalStuff(const tokenizer::TokenizerToken &token, ParserContext& context);

} // namespace states
} // namespace parser
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PARSER_STATES_HANDLING_NORMAL_STUFF_HPP
