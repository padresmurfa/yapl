#pragma once
#ifndef ORG_YAPLLANG_PARSER_STATES_HANDLE_END_OF_FILE_HPP
#define ORG_YAPLLANG_PARSER_STATES_HANDLE_END_OF_FILE_HPP

#include "include.hpp"
#include "parser_context.hpp"

namespace org {
namespace yapllang {
namespace parser {
    class ParserLines;
namespace states {

void handleEndOfFile(ParserLines &lines, ParserContext& context);

} // namespace states
} // namespace parser
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_PARSER_STATES_HANDLE_END_OF_FILE_HPP
