#include "parser_states.hpp"
#include "lexer/tokenizer/tokenizer.hpp"
namespace org {
namespace yapllang {
namespace parser {
namespace states {

std::string to_string(const ParserState state)
{
    // ##ParserStateMustStayInSync
    // when states are added, changed, or removed, then we must make sure that we keep various places in sync
    switch (state) {
        case ParserState::HANDLING_BEGIN_FILE: return "HANDLING_BEGIN_FILE";
        case ParserState::HANDLING_NORMAL_STUFF: return "HANDLING_NORMAL_STUFF";
        case ParserState::HANDLING_SINGLE_LINE_COMMENT: return "HANDLING_SINGLE_LINE_COMMENT";
        case ParserState::HANDLING_MULTI_LINE_COMMENT: return "HANDLING_MULTI_LINE_COMMENT";
        case ParserState::HANDLING_QUOTED_STRING: return "HANDLING_QUOTED_STRING";
        case ParserState::HANDLING_MULTI_LINE_STRING: return "HANDLING_MULTI_LINE_STRING";
        case ParserState::STARTING_INDENTED_BLOCK: return "STARTING_INDENTED_BLOCK";
        case ParserState::HANDLING_INDENTED_BLOCK: return "HANDLING_INDENTED_BLOCK";
        case ParserState::HANDLING_PARENTHESIS: return "HANDLING_PARENTHESIS";
        case ParserState::HANDLING_BRACKETS: return "HANDLING_BRACKETS";
        case ParserState::HANDLING_CURLY_BRACES: return "HANDLING_CURLY_BRACES";
        default:
            throw Exception("unexpected state");
    }
}

} // namespace states
} // namespace parser
} // namespace yapllang
} // namespace org
