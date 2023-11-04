#pragma once
#ifndef ORG_YAPLLANG_DECONTEXTUALIZER_STATES_HANDLING_MULTI_LINE_STRING_HPP
#define ORG_YAPLLANG_DECONTEXTUALIZER_STATES_HANDLING_MULTI_LINE_STRING_HPP

#include "include.hpp"
#include "decontextualizer_context.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace preprocessor {
    class PreprocessorToken;
}
namespace decontextualizer {
namespace states {

void handlingMultiLineString(const preprocessor::PreprocessorToken &token, DecontextualizerContext& context);

} // namespace states
} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_DECONTEXTUALIZER_STATES_HANDLING_MULTI_LINE_STRING_HPP
