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
    for (auto line : lines) {
        ParserContext context(line, stateStack, indentation);
        handleBeginOfLine(context);
        for (auto token : line.getTokens()) {
            auto currentState = context.getCurrentState();
            switch (currentState) {
                case ParserState::HANDLING_BEGIN_FILE:
                case ParserState::HANDLING_NORMAL_STUFF:
                    handlingNormalStuff(token, context);
                    break;
                case ParserState::HANDLING_SINGLE_LINE_COMMENT:
                    handlingSingleLineComment(token, context);
                    break;
                case ParserState::HANDLING_MULTI_LINE_COMMENT:
                    handlingMultiLineComment(token, context);
                    break;
                case ParserState::HANDLING_QUOTED_STRING:
                    handlingQuotedString(token, context);
                    break;
                case ParserState::HANDLING_MULTI_LINE_STRING:
                    handlingMultiLineString(token, context);
                    break;
                case ParserState::HANDLING_PARENTHESIS:
                    handlingParenthesis(token, context);
                    break;
                case ParserState::HANDLING_BRACKETS:
                    handlingBrackets(token, context);
                    break;
                case ParserState::HANDLING_CURLY_BRACES:
                    handlingCurlyBraces(token, context);
                    break;
                case ParserState::HANDLING_INDENTED_BLOCK:
                    handlingIndentedBlock(token, context);
                    break;
                default:
                    throw context.exception("unexpected state (" + to_string(currentState) + ") encountered during decontextualization");
            }
        }
        handleEndOfLine(context);
        auto lineToAdd = ParserLine(line, context.getOutputTokens());
        lineTokens.addLine(lineToAdd);
    }
    ParserContext eofContext(lines.getEOFAsTokenizerLine(), stateStack, indentation);
    handleEndOfFile(lineTokens, eofContext);
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
        auto beginLineNumber = line.getFileArea().getBegin().getLineNumber();
        auto beginLineOffset = line.getFileArea().getBegin().getLineOffsetInBytes();
        auto endLineNumber = line.getFileArea().getEnd().getLineNumber();
        auto endLineOffset = line.getFileArea().getEnd().getLineOffsetInBytes();
        std::cout << "[" << beginLineNumber << ":" << beginLineOffset << "]..[" << endLineNumber << ":" << endLineOffset << ">    " << line.toString() << std::endl;
    }
}

} // namespace parser
} // namespace yapllang
} // namespace org
