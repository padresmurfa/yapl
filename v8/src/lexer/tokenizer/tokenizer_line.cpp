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
    auto location = line_.getFileLocation();
    auto filename = location.getFilename();
    auto lineNumber = location.getLineNumber() + 1;
    auto fileOffset = location.getFileOffset() + lineLength;
    auto newLocation = lexer::file_reader::FileLocation(filename, lineNumber, fileOffset);
    auto newFileLine = lexer::file_reader::FileLine("", newLocation);
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

const lexer::file_reader::FileLocation& TokenizerLine::getFileLocation() const {
    return line_.getFileLocation();
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

void TokenizerLine::initializeTokens() {
    std::smatch match;
    std::string remainingText = lineWithoutWhitespace_;
    lexer::file_reader::FileLocation location = line_.getFileLocation().offsetByBytes(leadingWhitespace_.size());

    // #TokenizerTokenTypeNamesNeedToBeKeptInSync
    // #CharacterEscapesNeedToBeKeptInSync

    while (std::regex_search(remainingText, match, std::regex(R"((-{2,}|"""|"|\\[0-7]{1,3}|\\x[0-9A-Fa-F]+|\\u[0-9A-Fa-F]{4}|\\U[0-9A-Fa-F]{8}|\\[\"tnr\\bfva'\?]|:|\(|\)|\[|\]|\{|\}|\,))"))) {
        if (match.position() > 0) {
            // Add normal text before the match as a token
            auto normalText = remainingText.substr(0, match.position());
            tokens_.push_back({TokenizerTokenType::NORMAL, normalText, location});
            location = location.offsetByBytes(normalText.size());
        }

    // #TokenizerTokenTypeNamesNeedToBeKeptInSync
        auto matchedText = std::string(match[0]);
        // Determine the type of token
        if (matchedText == "\"\"\"") {
            tokens_.push_back({TokenizerTokenType::MULTI_LINE_STRING, matchedText, location});
        } else if (matchedText == "\"") {
            tokens_.push_back({TokenizerTokenType::QUOTED_STRING, matchedText, location});
        } else if (matchedText[0] == '\\') {
            tokens_.push_back({TokenizerTokenType::ESCAPED_CHARACTER, matchedText, location});
        } else if (matchedText == ":") {
            tokens_.push_back({TokenizerTokenType::COLON, matchedText, location});
        } else if (matchedText == "(") {
            tokens_.push_back({TokenizerTokenType::OPEN_PARENTHESIS, matchedText, location});
        } else if (matchedText == ")") {
            tokens_.push_back({TokenizerTokenType::CLOSE_PARENTHESIS, matchedText, location});
        } else if (matchedText == "[") {
            tokens_.push_back({TokenizerTokenType::OPEN_BRACKET, matchedText, location});
        } else if (matchedText == "]") {
            tokens_.push_back({TokenizerTokenType::CLOSE_BRACKET, matchedText, location});
        } else if (matchedText == "{") {
            tokens_.push_back({TokenizerTokenType::OPEN_CURLY_BRACE, matchedText, location});
        } else if (matchedText == "}") {
            tokens_.push_back({TokenizerTokenType::CLOSE_CURLY_BRACE, matchedText, location});
        } else if (matchedText == ",") {
            tokens_.push_back({TokenizerTokenType::COMMA, matchedText, location});
        } else if (matchedText[0] == '-') {
            TokenizerTokenType tokenType;
            if (matchedText.size() > 2) {
                tokenType = TokenizerTokenType::MINUS_MINUS_MINUS;
            } else {
                tokenType = TokenizerTokenType::MINUS_MINUS;
            }
            // NOTE: this will conflict if we add - or -- to the token list 
            tokens_.push_back({tokenType, matchedText, location});
        }
        if (!matchedText.empty()) {
            location = location.offsetByBytes(matchedText.size());
        }

        // Update the remaining text
        remainingText = match.suffix();
    }

    // Add any remaining normal text as a token
    if (!remainingText.empty()) {
        tokens_.push_back({TokenizerTokenType::NORMAL, remainingText, location});
    }
}


std::string TokenizerLine::toString() const {
    std::stringstream ss;
    ss
        << "=============================================" << std::endl
        << "TokenizerLine: \"" << getLineWithoutWhitespace() << "\"" << std::endl
        << "FileLine " << getFileLocation().toString()
        << " Leading Whitespace: " << getLeadingWhitespace().size()
        << " Tokens: " << std::endl;

    using tokenizer::TokenizerToken;
    using tokenizer::TokenizerTokenType;
    // #TokenizerTokenTypeNamesNeedToBeKeptInSync
    for (const TokenizerToken& token : getTokens()) {
        switch (token.type) {
            case TokenizerTokenType::QUOTED_STRING:
                ss << "  QUOTED_STRING: " << token.text << std::endl;
                break;
            case TokenizerTokenType::ESCAPED_CHARACTER:
                ss << "  ESCAPED_CHARACTER: " << token.text << std::endl;
                break;
            case TokenizerTokenType::MULTI_LINE_STRING:
                ss << "  MULTI_LINE_STRING: " << token.text << std::endl;
                break;
            case TokenizerTokenType::COLON:
                ss << "  COLON: " << token.text << std::endl;
                break;
            case TokenizerTokenType::OPEN_PARENTHESIS:
                ss << "  OPEN_PARENTHESIS: " << token.text << std::endl;
                break;
            case TokenizerTokenType::CLOSE_PARENTHESIS:
                ss << "  CLOSE_PARENTHESIS: " << token.text << std::endl;
                break;
            case TokenizerTokenType::OPEN_BRACKET:
                ss << "  OPEN_BRACKET: " << token.text << std::endl;
                break;
            case TokenizerTokenType::CLOSE_BRACKET:
                ss << "  CLOSE_BRACKET: " << token.text << std::endl;
                break;
            case TokenizerTokenType::OPEN_CURLY_BRACE:
                ss << "  OPEN_CURLY_BRACE: " << token.text << std::endl;
                break;
            case TokenizerTokenType::CLOSE_CURLY_BRACE:
                ss << "  CLOSE_CURLY_BRACE: " << token.text << std::endl;
                break;
            case TokenizerTokenType::COMMA:
                ss << "  COMMA: " << token.text << std::endl;
                break;
            case TokenizerTokenType::MINUS_MINUS:
                ss << "  MINUS_MINUS: " << token.text << std::endl;
                break;
            case TokenizerTokenType::MINUS_MINUS_MINUS:
                ss << "  MINUS_MINUS_MINUS: " << token.text << std::endl;
                break;
            case TokenizerTokenType::NORMAL:
                ss << "  NORMAL: " << token.text << std::endl;
                break;
            default:
                throw lexer::LexerException("oops");
        }
    }
    return ss.str();    
}

} // namespace tokenizer
} // namespace lexer
} // namespace yapllang
} // namespace org
