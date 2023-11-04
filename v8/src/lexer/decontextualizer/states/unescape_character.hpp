#pragma once
#ifndef ORG_YAPLLANG_DECONTEXTUALIZER_STATES_UNESCAPE_CHARACTER_HPP
#define ORG_YAPLLANG_DECONTEXTUALIZER_STATES_UNESCAPE_CHARACTER_HPP

#include "include.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace preprocessor {
    class PreprocessorToken;
}
namespace decontextualizer {
namespace states {

std::string unescapeCharacter(const std::string &escapedCharacter, const lexer::preprocessor::PreprocessorToken &token);

} // namespace states
} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org

#endif // ORG_YAPLLANG_DECONTEXTUALIZER_STATES_UNESCAPE_CHARACTER_HPP
