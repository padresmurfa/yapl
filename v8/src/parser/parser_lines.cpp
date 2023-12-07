#include "parser_lines.hpp"
#include "lexer/tokenizer/tokenizer.hpp"
#include "lexer/tokenizer/tokenizer_lines.hpp"
#include "parser_exception.hpp"
#include "states/parser_context.hpp"
#include "states/parser_states.hpp"
#include "states/handling_indented_block.hpp"
#include "states/handling_normal_stuff.hpp"
#include "states/handling_single_line_comment.hpp"
#include "states/handling_quoted_string.hpp"
#include "states/handling_multi_line_string.hpp"
#include "states/handling_multi_line_comment.hpp"
#include "states/handling_parenthesis.hpp"
#include "states/handling_brackets.hpp"
#include "states/handling_curly_braces.hpp"
#include "states/handle_begin_of_line.hpp"
#include "states/handle_end_of_file.hpp"
#include "states/handle_end_of_line.hpp"

namespace org {
namespace yapllang {
namespace parser {

using states::ParserState;
using states::ParserContext;
using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;

ParserLines::ParserLines() {
}

ParserLines::ParserLines(const ParserLines& other)
    : lines_(other.lines_)
{
}

ParserLines& ParserLines::operator=(const ParserLines& other) {
    if (this != &other) {
        lines_ = other.lines_;
    }
    return *this;
}

void ParserLines::addLine(const ParserLine& line) {
    lines_.emplace_back(line);
}

ParserLines::iterator ParserLines::begin() const {
    return lines_.begin();
}

ParserLines::iterator ParserLines::end() const {
    return lines_.end();
}

ParserLines ParserLines::parse(const lexer::tokenizer::TokenizerLines& lines) {
    ParserLines lineTokens;
    std::vector<ParserState> stateStack;
    std::vector<size_t> indentation;
    stateStack.push_back(ParserState::HANDLING_BEGIN_FILE);
    size_t line_number = 0;
    for (auto line : lines) {
        ParserContext context(line, stateStack, indentation);
        BEGIN_SECTION()
        handleBeginOfLine(context);
        END_SECTION("handleBeginOfLine")
        for (auto token : line.getTokens()) {
            auto currentState = context.getCurrentState();
            switch (currentState) {
                case ParserState::HANDLING_BEGIN_FILE:
                case ParserState::HANDLING_NORMAL_STUFF:
                    BEGIN_SECTION()
                    handlingNormalStuff(token, context);
                    END_SECTION("handlingNormalStuff")
                    break;
                case ParserState::HANDLING_SINGLE_LINE_COMMENT:
                    BEGIN_SECTION()
                    handlingSingleLineComment(token, context);
                    END_SECTION("handlingSingleLineComment")
                    break;
                case ParserState::HANDLING_MULTI_LINE_COMMENT:
                    BEGIN_SECTION()
                    handlingMultiLineComment(token, context);
                    END_SECTION("handlingMultiLineComment")
                    break;
                case ParserState::HANDLING_QUOTED_STRING:
                    BEGIN_SECTION()
                    handlingQuotedString(token, context);
                    END_SECTION("handlingQuotedString")
                    break;
                case ParserState::HANDLING_MULTI_LINE_STRING:
                    BEGIN_SECTION()
                    handlingMultiLineString(token, context);
                    END_SECTION("handlingMultiLineString")
                    break;
                case ParserState::HANDLING_PARENTHESIS:
                    BEGIN_SECTION()
                    handlingParenthesis(token, context);
                    END_SECTION("handlingParenthesis")
                    break;
                case ParserState::HANDLING_BRACKETS:
                    BEGIN_SECTION()
                    handlingBrackets(token, context);
                    END_SECTION("handlingBrackets")
                    break;
                case ParserState::HANDLING_CURLY_BRACES:
                    BEGIN_SECTION()
                    handlingCurlyBraces(token, context);
                    END_SECTION("handlingCurlyBraces")
                    break;
                case ParserState::HANDLING_INDENTED_BLOCK:
                    BEGIN_SECTION()
                    handlingIndentedBlock(token, context);
                    END_SECTION("handlingIndentedBlock")
                    break;
                default:
                    throw context.exception("unexpected state (" + to_string(currentState) + ") encountered during decontextualization");
            }
        }
        BEGIN_SECTION()
        handleEndOfLine(context);
        END_SECTION("handleEndOfLine")
        auto lineToAdd = ParserLine(line, context.getOutputTokens());
        lineTokens.addLine(lineToAdd);
    }
    ParserContext eofContext(lines.getEOFAsTokenizerLine(), stateStack, indentation);
    BEGIN_SECTION()
    handleEndOfFile(lineTokens, eofContext);
    END_SECTION("handleEndOfFile")
    if (!eofContext.getOutputTokens().empty())
    {
        auto lineToAdd = ParserLine(eofContext.getCurrentLine(), eofContext.getOutputTokens());
        lineTokens.addLine(lineToAdd);
    }
    return lineTokens;
}

std::vector<ParserLine> &ParserLines::mutate() {
    return lines_;
}

void ParserLines::print() const {

    // TODO: this is copy-pasta with TokenizerLines, deal with it

    // Print the tokens per line
    for (const ParserLine& line : lines_) {
        auto begin = line.getFileArea().getBegin();
        auto beginLineNumber = begin.getLineNumber();
        auto beginLineOffset = begin.getLineOffsetInBytes();
        auto beginFileOffset = begin.getFileOffset();
        auto end = line.getFileArea().getEnd();
        auto endLineNumber = end.getLineNumber();
        auto endLineOffset = end.getLineOffsetInBytes();
        auto endFileOffset = end.getFileOffset();
        std::cout   << "[" << beginFileOffset << "|" << beginLineNumber << ":" << beginLineOffset << "]..["
                    << endFileOffset << "|" <<endLineNumber << ":" << endLineOffset << ">    "
                    << line.toString()
                    << std::endl;
    }
}

} // namespace parser
} // namespace yapllang
} // namespace org
