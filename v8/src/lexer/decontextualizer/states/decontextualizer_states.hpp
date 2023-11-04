#pragma once
#ifndef ORG_YAPLLANG_DECONTEXTUALIZER_STATES_HPP
#define ORG_YAPLLANG_DECONTEXTUALIZER_STATES_HPP

#include "include.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {
namespace states {

// #DecontextualizerStateMustStayInSync
enum class DecontextualizerState {
    HANDLING_BEGIN_FILE,
    HANDLING_NORMAL_STUFF,
    HANDLING_SINGLE_LINE_COMMENT,
    HANDLING_SEMANTIC_COMMENT,
    HANDLING_MULTI_LINE_COMMENT,
    HANDLING_QUOTED_STRING,
    HANDLING_MULTI_LINE_STRING,
    STARTING_INDENTED_BLOCK,
    HANDLING_INDENTED_BLOCK,
    HANDLING_PARENTHESIS,
    HANDLING_BRACKETS,
    HANDLING_CURLY_BRACES
};

std::string to_string(const DecontextualizerState state);

} // namespace states
} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_DECONTEXTUALIZER_STATES_HPP
