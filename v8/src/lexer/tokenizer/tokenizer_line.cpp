#include "tokenizer_line.hpp"
#include "lexer/file_reader/file_line.hpp"
#include "lexer/lexer_exception.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace tokenizer {

using namespace org::yapllang;

TokenizerLine::TokenizerLine() {
}

TokenizerLine::TokenizerLine(const lexer::file_reader::FileLine& line) : line_(line) {
    initializeText();
    initializeTokens();
}

TokenizerLine::TokenizerLine(const TokenizerLine& other)
    : line_(other.line_)
    , leadingWhitespace_(other.leadingWhitespace_)
    , trailingWhitespace_(other.trailingWhitespace_)
    , lineWithoutWhitespace_(other.lineWithoutWhitespace_)
    , tokens_(other.tokens_)
{
}

TokenizerLine TokenizerLine::atEOF() const {
    auto lineLength = line_.getText().size();
    auto area = line_.getFileArea();
    auto newArea = file_reader::FileArea(area.getFilename(), area.getEnd(), area.getEnd());
    auto newFileLine = lexer::file_reader::FileLine("", newArea);
    TokenizerLine result(newFileLine);
    return result;
}

TokenizerLine& TokenizerLine::operator=(const TokenizerLine& other) {
    if (this != &other) {
        line_ = other.line_;
        leadingWhitespace_ = other.leadingWhitespace_;
        trailingWhitespace_ = other.trailingWhitespace_;
        lineWithoutWhitespace_ = other.lineWithoutWhitespace_;
        tokens_ = other.tokens_;
    }
    return *this;   
}

bool TokenizerLine::empty() const {
    return lineWithoutWhitespace_.empty();
}

const lexer::file_reader::FileLine& TokenizerLine::getFileLine() const {
    return line_;
}

const lexer::file_reader::FileArea TokenizerLine::getFileArea() const {
    return line_.getFileArea();
}

const std::string& TokenizerLine::getLeadingWhitespace() const {
    return leadingWhitespace_;
}

const std::string& TokenizerLine::getTrailingWhitespace() const {
    return trailingWhitespace_;
}

const std::string& TokenizerLine::getLineWithoutWhitespace() const {
    return lineWithoutWhitespace_;
}

const std::vector<TokenizerToken>& TokenizerLine::getTokens() const {
    return tokens_;
}

void TokenizerLine::initializeText() {
    auto text = line_.getText();
    size_t leadingWhitespaceLength = 0;
    while (leadingWhitespaceLength < text.size() && (text[leadingWhitespaceLength] == ' ' || text[leadingWhitespaceLength] == '\t')) {
        if (text[leadingWhitespaceLength] == '\t') {
            // Treat tabs as-is, without converting to spaces
            ++leadingWhitespaceLength;
            break;
        }
        ++leadingWhitespaceLength;
    }
    leadingWhitespace_ = text.substr(0, leadingWhitespaceLength);

    size_t trailingWhitespaceLength = 0;
    for (size_t i = text.size(); i > 0; --i) {
        if (text[i - 1] == ' ' || text[i - 1] == '\t') {
            if (text[i - 1] == '\t') {
                // Treat tabs as-is, without converting to spaces
                ++trailingWhitespaceLength;
                break;
            }
            ++trailingWhitespaceLength;
        } else {
            break;
        }
    }
    trailingWhitespace_ = text.substr(text.size() - trailingWhitespaceLength);

    // Remove leading and trailing whitespace from the line
    lineWithoutWhitespace_ = text.substr(leadingWhitespaceLength, text.size() - trailingWhitespaceLength - leadingWhitespaceLength);
}

void stripSurroundingWhitespace(std::string& text) {
    int trimFirst = 0;
    for (auto it = text.begin(); it != text.end(); it++) {
        if (std::isspace(*it)) {
            trimFirst++;
        } else {
            break;
        }
    }
    int trimLast = 0;
    for (auto it = text.rbegin(); it != text.rend(); it++) {
        if (std::isspace(*it)) {
            trimLast++;
        } else {
            break;
        }
    }
    if (trimFirst > 0 || trimLast > 0) {
        text = text.substr(trimFirst, text.length() - trimLast - trimFirst);
    }
}

void TokenizerLine::initializeTokens() {
    std::smatch match;
    std::string remainingText = lineWithoutWhitespace_;
    lexer::file_reader::FileLocation newBeginLocation = line_.getFileArea().getBegin().offsetByBytes(leadingWhitespace_.size());
    lexer::file_reader::FileLocation newEndLocation = newBeginLocation;
    file_reader::FileArea newArea = file_reader::FileArea(line_.getFileArea().getFilename(), newBeginLocation, newEndLocation);

    // #TokenizerTokenTypeNamesNeedToBeKeptInSync
    // #CharacterEscapesNeedToBeKeptInSync

    while (std::regex_search(remainingText, match, std::regex(R"((-{2,}|"""|"|\\0[0-7]{1,3}|\\x[0-9A-Fa-F]{1,6}|\\u[0-9A-Fa-F]{4}|\\U[0-9A-Fa-F]{8}|\\[\"tnr\\bfvae'\?]|:|\(|\)|\[|\]|\{|\}|\,))"))) {
        if (match.position() > 0) {
            // Add normal text before the match as a token
            auto normalText = remainingText.substr(0, match.position());
            newEndLocation = newBeginLocation.offsetByBytes(normalText.size());
            newArea = file_reader::FileArea(newArea.getFilename(), newBeginLocation, newEndLocation);
            stripSurroundingWhitespace(normalText);
            tokens_.push_back({TokenizerTokenType::NORMAL, normalText, newArea});
            newBeginLocation = newEndLocation;
        }

    // #TokenizerTokenTypeNamesNeedToBeKeptInSync
        auto matchedText = std::string(match[0]);
        newEndLocation = newBeginLocation.offsetByBytes(matchedText.size());
        newArea = file_reader::FileArea(newArea.getFilename(), newBeginLocation, newEndLocation);
        // Determine the type of token
        if (matchedText == "\"\"\"") {
            tokens_.push_back({TokenizerTokenType::MULTI_LINE_STRING, matchedText, newArea});
        } else if (matchedText == "\"") {
            tokens_.push_back({TokenizerTokenType::QUOTED_STRING, matchedText, newArea});
        } else if (matchedText[0] == '\\') {
            tokens_.push_back({TokenizerTokenType::ESCAPED_CHARACTER, matchedText, newArea});
        } else if (matchedText == ":") {
            tokens_.push_back({TokenizerTokenType::COLON, matchedText, newArea});
        } else if (matchedText == "(") {
            tokens_.push_back({TokenizerTokenType::OPEN_PARENTHESIS, matchedText, newArea});
        } else if (matchedText == ")") {
            tokens_.push_back({TokenizerTokenType::CLOSE_PARENTHESIS, matchedText, newArea});
        } else if (matchedText == "[") {
            tokens_.push_back({TokenizerTokenType::OPEN_BRACKET, matchedText, newArea});
        } else if (matchedText == "]") {
            tokens_.push_back({TokenizerTokenType::CLOSE_BRACKET, matchedText, newArea});
        } else if (matchedText == "{") {
            tokens_.push_back({TokenizerTokenType::OPEN_CURLY_BRACE, matchedText, newArea});
        } else if (matchedText == "}") {
            tokens_.push_back({TokenizerTokenType::CLOSE_CURLY_BRACE, matchedText, newArea});
        } else if (matchedText == ",") {
            tokens_.push_back({TokenizerTokenType::COMMA, matchedText, newArea});
        } else if (matchedText[0] == '-') {
            TokenizerTokenType tokenType;
            if (matchedText.size() > 2) {
                tokenType = TokenizerTokenType::MINUS_MINUS_MINUS;
            } else {
                tokenType = TokenizerTokenType::MINUS_MINUS;
            }
            // NOTE: this will conflict if we add - or -- to the token list 
            tokens_.push_back({tokenType, matchedText, newArea});
        }
        if (!matchedText.empty()) {
            newBeginLocation = newEndLocation;
            newArea = file_reader::FileArea(newArea.getFilename(), newBeginLocation, newEndLocation);
        }

        // Update the remaining text
        remainingText = match.suffix();
    }

    // Add any remaining normal text as a token
    if (!remainingText.empty()) {
        newArea = file_reader::FileArea(newArea.getFilename(), newArea.getBegin(), line_.getFileArea().getEnd());
        stripSurroundingWhitespace(remainingText);
        tokens_.push_back({TokenizerTokenType::NORMAL, remainingText, newArea});
    }
}


std::string TokenizerLine::toString() const {
    std::stringstream ss;
    ss
        << "=============================================" << std::endl
        << "TokenizerLine: \"" << getLineWithoutWhitespace() << "\"" << std::endl
        << "FileArea " << getFileArea().toString()
        << " Leading Whitespace: " << getLeadingWhitespace().size()
        << " Tokens: " << std::endl;

    using tokenizer::TokenizerToken;
    using tokenizer::TokenizerTokenType;
    // #TokenizerTokenTypeNamesNeedToBeKeptInSync
    for (const TokenizerToken& token : getTokens()) {
        ss << token.toString() << std::endl;
    }
    return ss.str();    
}

} // namespace tokenizer
} // namespace lexer
} // namespace yapllang
} // namespace org
