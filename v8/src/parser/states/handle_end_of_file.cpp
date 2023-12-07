#include "handle_end_of_file.hpp"
#include "../parser_lines.hpp"

namespace org {
namespace yapllang {
namespace parser {
namespace states {

using states::ParserState;
using states::ParserContext;
using lexer::tokenizer::TokenizerToken;
using lexer::tokenizer::TokenizerTokenType;

bool maybeMergeAdjacentSingleLineComments(std::vector<ParserLine>::iterator &previousLine, std::vector<ParserLine>::iterator &currentLine) {
    // TODO: fix so that this code catches this kind of scenario:
    // asdf -- asdffsadfsda
    //      -- asdfasdf
    std::vector<ParserToken>& previousLineTokens = previousLine->mutateTokens();
    const std::vector<ParserToken>& currentLineTokens = currentLine->getTokens();
    auto hasSingleToken = previousLineTokens.size() == 1 && currentLineTokens.size() == 1;
    if (hasSingleToken) {
        ParserToken &previousToken = previousLineTokens[0];
        const ParserToken &currentToken = currentLineTokens[0];
        auto areBothSingleLineComments = previousToken.type == ParserTokenType::TMP_SINGLE_LINE_COMMENT_CONTENT && currentToken.type == ParserTokenType::TMP_SINGLE_LINE_COMMENT_CONTENT;
        if (areBothSingleLineComments) {
            // xcxc TODO use leading whitespace to allow immediate predecessor to match
            // currentLine->getTokenizerLine().getLeadingWhitespace();
            auto isPredecessorLineOf = previousToken.isPredecessorLineOf(currentToken);
            if (isPredecessorLineOf) {
                previousToken.text.append("\n");
                if (currentToken.text.size() > 2 && std::isspace(currentToken.text[2])) {
                    previousToken.text.append(currentToken.text.substr(3));
                } else {
                    previousToken.text.append(currentToken.text.substr(2));
                }
                previousToken.area.extendTo(currentToken.area);
                return true;
            }
        }
    }
    return false;
}

bool maybeMergeEmptyLineWithPriorLine(std::vector<ParserLine>::iterator &previousLine, std::vector<ParserLine>::iterator &currentLine) 
{
    if (currentLine->empty()) {
        previousLine->mutateTokens().rbegin()->area.extendTo(currentLine->getFileArea());
        switch (previousLine->getTokens().rbegin()->type) {
            case ParserTokenType::TMP_BEGIN_MULTI_LINE_COMMENT:
            case ParserTokenType::TMP_BEGIN_MULTI_LINE_STRING:
            case ParserTokenType::TMP_STRING_CONTENT: // assuming that we're in a multi-line-string
            case ParserTokenType::TMP_MULTI_LINE_COMMENT_CONTENT:
                previousLine->mutateTokens().rbegin()->text.append("\n");
                break;
            default:
                break;
        }
        return true;
    }
    return false;
}

bool maybeMergeAdjacentMultiLineComments(std::vector<ParserLine>::iterator &previousLine, std::vector<ParserLine>::iterator &currentLine) {
    std::vector<ParserToken>& previousLineTokens = previousLine->mutateTokens();
    const std::vector<ParserToken>& currentLineTokens = currentLine->getTokens();
    auto hasTokens = previousLineTokens.size() >= 1 && currentLineTokens.size() == 1;
    if (hasTokens) {
        ParserToken & previousToken = previousLineTokens.back();
        const ParserToken &currentToken = currentLineTokens.front();
        auto isPreviousMultiLineComment = (previousToken.type == ParserTokenType::TMP_BEGIN_MULTI_LINE_COMMENT) || (previousToken.type == ParserTokenType::TMP_MULTI_LINE_COMMENT_CONTENT);
        auto isCurrentMultiLineComment = (currentToken.type == ParserTokenType::TMP_END_MULTI_LINE_COMMENT) || (currentToken.type == ParserTokenType::TMP_MULTI_LINE_COMMENT_CONTENT);
        if (isPreviousMultiLineComment && isCurrentMultiLineComment) {
            if (currentToken.type == ParserTokenType::TMP_END_MULTI_LINE_COMMENT) {
                previousToken.area.extendTo(currentToken.area);
                return true;
            }
            auto prevWS = previousLine->getTokenizerLine().getLeadingWhitespace();
            auto currWS = currentLine->getTokenizerLine().getLeadingWhitespace();
            int shouldIndent = currWS.size() > prevWS.size();
            if (previousToken.type != ParserTokenType::TMP_BEGIN_MULTI_LINE_COMMENT) {
                previousToken.text.append("\n");
                if (shouldIndent) {
                    previousToken.text.append(currWS.substr(prevWS.size()));
                }
            }
            previousToken.type = ParserTokenType::TMP_MULTI_LINE_COMMENT_CONTENT;
            previousToken.text.append(currentToken.text);
            if (shouldIndent) {
                previousToken.text.append(currWS.substr(prevWS.size()));
            }
            previousToken.area.extendTo(currentToken.area);
            return true;
        }
    }
    return false;
}

bool maybeMergeAdjacentMultiLineStrings(std::vector<ParserLine>::iterator &previousLine, std::vector<ParserLine>::iterator &currentLine) {
    std::vector<ParserToken>& previousLineTokens = previousLine->mutateTokens();
    const std::vector<ParserToken>& currentLineTokens = currentLine->getTokens();
    auto hasTokens = previousLineTokens.size() >= 1 && currentLineTokens.size() == 1;
    if (hasTokens) {
        ParserToken & previousToken = previousLineTokens.back();
        const ParserToken &currentToken = currentLineTokens.front();
        auto isPreviousMultiLineString = (previousToken.type == ParserTokenType::TMP_BEGIN_MULTI_LINE_STRING) || (previousToken.type == ParserTokenType::TMP_STRING_CONTENT);
        auto isCurrentMultiLineString = (currentToken.type == ParserTokenType::TMP_END_MULTI_LINE_STRING) || (currentToken.type == ParserTokenType::TMP_STRING_CONTENT);
        if (isPreviousMultiLineString && isCurrentMultiLineString) {
            if (previousToken.type != ParserTokenType::TMP_BEGIN_MULTI_LINE_STRING) {
                // TODO: empty lines are wreaking havoc... deal with that
                previousToken.text.append("\n");
            }
            previousToken.type = ParserTokenType::TMP_STRING_CONTENT;
            previousToken.text.append(currentToken.text);
            previousToken.area.extendTo(currentToken.area);
            return true;
        }
    }
    return false;
}

bool maybeMergeParserLines(std::vector<ParserLine>::iterator &currentLine) {
    /*
    TODO: multi-line constructs should be merged at this point in time
    */
    std::vector<ParserLine>::iterator previousLine = std::prev(currentLine);
    if (maybeMergeEmptyLineWithPriorLine(previousLine, currentLine)) {
        return true;
    }
    if (maybeMergeAdjacentMultiLineComments(previousLine, currentLine)) {
        return true;
    }
    if (maybeMergeAdjacentSingleLineComments(previousLine, currentLine)) {
        return true;
    }
    if (maybeMergeAdjacentMultiLineStrings(previousLine, currentLine)) {
        return true;
    }
    return false;
}

void stripCommentAndStringDeliminators(std::vector<ParserLine> &parserLines) {
    size_t line_number = 0;
    for (auto it = parserLines.begin(); it != parserLines.end(); it++) {
        std::vector<ParserToken>& mutableTokens = it->mutateTokens();
        if (!mutableTokens.empty()) {
            ParserToken& lastToken = *(mutableTokens.rbegin());
            switch (lastToken.type) {
                case ParserTokenType::TMP_SINGLE_LINE_COMMENT_CONTENT:
                    // TODO: move this into the end-of-line handler
                    BEGIN_SECTION()
                    BEGIN_SECTION()
                    if (lastToken.text.size() > 2 && std::isspace(lastToken.text[2])) {
                        mutableTokens.rbegin()->text = lastToken.text.substr(3);
                    } else {
                        mutableTokens.rbegin()->text = lastToken.text.substr(2);
                    }
                    END_SECTION(lastToken.text)
                    END_SECTION("TMP_SINGLE_LINE_COMMENT_CONTENT")
                    break;
                case ParserTokenType::TMP_BEGIN_MULTI_LINE_STRING:
                case ParserTokenType::TMP_END_MULTI_LINE_STRING:
                    BEGIN_SECTION()
                    mutableTokens.rbegin()->text = "";
                    END_SECTION("TMP_..._MULTI_LINE_STRING")
                    break;
                default:
                    break;
            }
        }
    }    
}

void replaceTmpParserTokenTypesWithRealOnes(std::vector<ParserLine> &parserLines) {
    for (auto it = parserLines.begin(); it != parserLines.end(); it++) {
        std::vector<ParserToken>& mutableTokens = it->mutateTokens();
        if (!mutableTokens.empty()) {
            ParserToken& lastToken = *(mutableTokens.rbegin());
            switch (lastToken.type) {
                case ParserTokenType::TMP_MULTI_LINE_COMMENT_CONTENT:
                case ParserTokenType::TMP_SINGLE_LINE_COMMENT_CONTENT:
                    mutableTokens.rbegin()->type = ParserTokenType::COMMENT;
                    break;
                case ParserTokenType::TMP_STRING_CONTENT:
                    mutableTokens.rbegin()->type = ParserTokenType::STRING;
                    break;
                default:
                    break;
            }
        }
    }    
}

void normalizeMultiLineLeadingWhiteSpace(std::vector<ParserLine> &parserLines) {
    int leadingWhitespace = -1;
    for (auto it = parserLines.begin(); it != parserLines.end(); it++) {
        std::vector<ParserToken>& mutableTokens = it->mutateTokens();
        if (!mutableTokens.empty()) {
            ParserToken& lastToken = *(mutableTokens.rbegin());
            if (lastToken.type == ParserTokenType::TMP_BEGIN_MULTI_LINE_COMMENT) {
                leadingWhitespace = it->getTokenizerLine().getLeadingWhitespace().size();
            } else if (lastToken.type == ParserTokenType::TMP_BEGIN_MULTI_LINE_STRING) {
                leadingWhitespace = 4 + it->getTokenizerLine().getLeadingWhitespace().size();
            } else if (leadingWhitespace >= 0 && (lastToken.type == ParserTokenType::TMP_MULTI_LINE_COMMENT_CONTENT || lastToken.type == ParserTokenType::TMP_STRING_CONTENT)) {
                // TODO: assert that there is only a single token in this line
                int currentWhitespace = it->getTokenizerLine().getLeadingWhitespace().size();
                int incorrectSpaces = currentWhitespace - leadingWhitespace;
                if (incorrectSpaces != 0) {
                    lexer::file_reader::FileArea& area = mutableTokens.rbegin()->area;
                    mutableTokens.rbegin()->area = lexer::file_reader::FileArea(
                        area.getFilename(),
                        area.getBegin().offsetByBytes(-incorrectSpaces),
                        area.getEnd()
                    );
                    if (incorrectSpaces > 0) {
                        auto ws = std::string(incorrectSpaces, ' ');
                        mutableTokens.rbegin()->text = ws + mutableTokens.rbegin()->text;
                    }
                }
            } else if ((lastToken.type == ParserTokenType::TMP_END_MULTI_LINE_COMMENT) || (lastToken.type == ParserTokenType::TMP_END_MULTI_LINE_STRING)) {
                leadingWhitespace = -1;
            }
        }
    }    
}

void handleEndOfFile(ParserLines &lines, ParserContext& context) {
    bool loop = true;
    while (loop) {
        loop = false;
        auto state = context.getCurrentState();
        switch (state) {
            case ParserState::HANDLING_BEGIN_FILE:
                break;

            case ParserState::HANDLING_NORMAL_STUFF:
                break;

            case ParserState::HANDLING_SINGLE_LINE_COMMENT:
                {
                    BEGIN_SECTION()
                    auto eol = context.getCurrentLine().getFileArea().asEndOfArea();
                    context.pop(ParserState::HANDLING_SINGLE_LINE_COMMENT);
                    ParserToken newToken({
                        ParserTokenType::TMP_END_SINGLE_LINE_COMMENT,
                        "",
                        eol
                    });
                    context.pushOutputToken(newToken);
                    loop = true;
                    END_SECTION("HANDLING_SINGLE_LINE_COMMENT")
                }
                break;

            case ParserState::HANDLING_MULTI_LINE_COMMENT:
                throw context.unclosedOpenedBlockException("missing multi-line comment terminator");

            case ParserState::HANDLING_MULTI_LINE_STRING:
                throw context.unclosedOpenedBlockException("missing multi-line string terminator");

            case ParserState::HANDLING_PARENTHESIS:
                throw context.unclosedOpenedBlockException("missing closing parenthesis");

            case ParserState::HANDLING_BRACKETS:
                throw context.unclosedOpenedBlockException("missing closing bracket");

            case ParserState::HANDLING_CURLY_BRACES:
                throw context.unclosedOpenedBlockException("missing closing curly braces");

            case ParserState::HANDLING_QUOTED_STRING:
                throw context.unclosedOpenedBlockException("missing closing quote");

            case ParserState::STARTING_INDENTED_BLOCK:
                throw context.unclosedOpenedBlockException("expected indented block following :");

            case ParserState::HANDLING_INDENTED_BLOCK:
                {
                    BEGIN_SECTION()
                    auto eol = context.getCurrentLine().getFileArea().asEndOfArea();
                    int dedents = context.maybeDedent("");
                    while (dedents-- > 0) {
                        context.pop(ParserState::HANDLING_INDENTED_BLOCK);
                        ParserToken newToken({
                            ParserTokenType::END_BLOCK,
                            "",
                            eol
                        });
                        context.pushOutputToken(newToken);
                    }
                    END_SECTION("HANDLING_INDENTED_BLOCK")
                }
                break;

            default:
                throw context.exception("unexpected state (" + to_string(state) + "=" + std::to_string(static_cast<int>(state)) + ") at EOF");
        }
    }
    if (context.getCurrentState() != ParserState::HANDLING_BEGIN_FILE) {
        throw context.parserException("context state not empty at end-of-file");
    }
    std::vector<ParserLine> &parserLines = lines.mutate();
    BEGIN_SECTION()
    auto it = parserLines.begin();
    while (it != parserLines.end()) {
        if (it != parserLines.begin() && maybeMergeParserLines(it)) {
            it = parserLines.erase(it);
        } else {
            ++it;
        }
    }
    END_SECTION("while (it != parserLines.end())")
    BEGIN_SECTION()
    stripCommentAndStringDeliminators(parserLines);
    END_SECTION("stripCommentAndStringDeliminators")
    BEGIN_SECTION()
    normalizeMultiLineLeadingWhiteSpace(parserLines);
    END_SECTION("normalizeMultiLineLeadingWhiteSpace")
    BEGIN_SECTION()
    replaceTmpParserTokenTypesWithRealOnes(parserLines);
    END_SECTION("replaceTmpParserTokenTypesWithRealOnes")
}

} // namespace states
} // namespace parser
} // namespace yapllang
} // namespace org
