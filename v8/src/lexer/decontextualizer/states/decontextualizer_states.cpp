#include "decontextualizer_states.hpp"
#include "lexer/preprocessor/preprocessor.hpp"
namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {
namespace states {

std::string to_string(const DecontextualizerState state)
{
    // ##DecontextualizerStateMustStayInSync
    // when states are added, changed, or removed, then we must make sure that we keep various places in sync
    switch (state) {
        case DecontextualizerState::HANDLING_BEGIN_FILE: return "HANDLING_BEGIN_FILE";
        case DecontextualizerState::HANDLING_NORMAL_STUFF: return "HANDLING_NORMAL_STUFF";
        case DecontextualizerState::HANDLING_SINGLE_LINE_COMMENT: return "HANDLING_SINGLE_LINE_COMMENT";
        case DecontextualizerState::HANDLING_QUOTED_STRING: return "HANDLING_QUOTED_STRING";
        case DecontextualizerState::HANDLING_MULTI_LINE_STRING: return "HANDLING_MULTI_LINE_STRING";
        case DecontextualizerState::STARTING_INDENTED_BLOCK: return "STARTING_INDENTED_BLOCK";
        case DecontextualizerState::HANDLING_INDENTED_BLOCK: return "HANDLING_INDENTED_BLOCK";
        case DecontextualizerState::HANDLING_PARENTHESIS: return "HANDLING_PARENTHESIS";
        case DecontextualizerState::HANDLING_BRACKETS: return "HANDLING_BRACKETS";
        case DecontextualizerState::HANDLING_CURLY_BRACES: return "HANDLING_CURLY_BRACES";
        default:
            throw Exception("unexpected state");
    }
}

} // namespace states
} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org
