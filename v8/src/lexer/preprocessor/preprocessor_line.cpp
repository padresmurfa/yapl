#include "preprocessor_line.hpp"
#include "lexer/file_reader/file_line.hpp"
#include "lexer/lexer_exception.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace preprocessor {

using namespace org::yapllang;

PreprocessorLine::PreprocessorLine() {
}

PreprocessorLine::PreprocessorLine(const lexer::file_reader::FileLine& line) : line_(line) {
    initializeText();
    initializeTokens();
}

PreprocessorLine::PreprocessorLine(const PreprocessorLine& other)
    : line_(other.line_)
    , leadingWhitespace_(other.leadingWhitespace_)
    , trailingWhitespace_(other.trailingWhitespace_)
    , lineWithoutWhitespace_(other.lineWithoutWhitespace_)
    , tokens_(other.tokens_)
{
}

PreprocessorLine PreprocessorLine::atEOF() const {
    auto lineLength = line_.getText().size();
    auto location = line_.getFileLocation();
    auto filename = location.getFilename();
    auto lineNumber = location.getLineNumber() + 1;
    auto fileOffsetInBytes = location.getFileOffsetInBytes() + lineLength;
    auto newLocation = lexer::file_reader::FileLocation(filename, lineNumber, fileOffsetInBytes);
    auto newFileLine = lexer::file_reader::FileLine("", newLocation);
    PreprocessorLine result(newFileLine);
    return result;
}

PreprocessorLine& PreprocessorLine::operator=(const PreprocessorLine& other) {
    if (this != &other) {
        line_ = other.line_;
        leadingWhitespace_ = other.leadingWhitespace_;
        trailingWhitespace_ = other.trailingWhitespace_;
        lineWithoutWhitespace_ = other.lineWithoutWhitespace_;
        tokens_ = other.tokens_;
    }
    return *this;   
}

bool PreprocessorLine::empty() const {
    return lineWithoutWhitespace_.empty();
}

const lexer::file_reader::FileLine& PreprocessorLine::getFileLine() const {
    return line_;
}

const lexer::file_reader::FileLocation& PreprocessorLine::getFileLocation() const {
    return line_.getFileLocation();
}

const std::string& PreprocessorLine::getLeadingWhitespace() const {
    return leadingWhitespace_;
}

const std::string& PreprocessorLine::getTrailingWhitespace() const {
    return trailingWhitespace_;
}

const std::string& PreprocessorLine::getLineWithoutWhitespace() const {
    return lineWithoutWhitespace_;
}

const std::vector<PreprocessorToken>& PreprocessorLine::getTokens() const {
    return tokens_;
}

void PreprocessorLine::initializeText() {
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

void PreprocessorLine::initializeTokens() {
    std::smatch match;
    std::string remainingText = lineWithoutWhitespace_;
    lexer::file_reader::FileLocation location = line_.getFileLocation().offsetByBytes(leadingWhitespace_.size());

    // #PreprocessorTokenTypeNamesNeedToBeKeptInSync
    // #CharacterEscapesNeedToBeKeptInSync

    while (std::regex_search(remainingText, match, std::regex(R"((\/\/|;|\/\*|\*\/|"""|"|\\[0-7]{1,3}|\\x[0-9A-Fa-F]+|\\u[0-9A-Fa-F]{4}|\\U[0-9A-Fa-F]{8}|\\[\"tnr\\bfva'\?]|:|\(|\)|\[|\]|\{|\}|\,))"))) {
        if (match.position() > 0) {
            // Add normal text before the match as a token
            auto normalText = remainingText.substr(0, match.position());
            tokens_.push_back({PreprocessorTokenType::NORMAL, normalText, location});
            location = location.offsetByBytes(normalText.size());
        }

    // #PreprocessorTokenTypeNamesNeedToBeKeptInSync
        auto matchedText = std::string(match[0]);
        // Determine the type of token
        if (matchedText == "//") {
            tokens_.push_back({PreprocessorTokenType::SINGLE_LINE_COMMENT, matchedText, location});
        } else if (matchedText == ";") {
            tokens_.push_back({PreprocessorTokenType::SEMICOLON, matchedText, location});
        } else if (matchedText == "/*") {
            tokens_.push_back({PreprocessorTokenType::BEGIN_MULTI_LINE_COMMENT, matchedText, location});
        } else if (matchedText == "*/") {
            tokens_.push_back({PreprocessorTokenType::END_MULTI_LINE_COMMENT, matchedText, location});
        } else if (matchedText == "\"\"\"") {
            tokens_.push_back({PreprocessorTokenType::MULTI_LINE_STRING, matchedText, location});
        } else if (matchedText == "\"") {
            tokens_.push_back({PreprocessorTokenType::QUOTED_STRING, matchedText, location});
        } else if (matchedText[0] == '\\') {
            tokens_.push_back({PreprocessorTokenType::ESCAPED_CHARACTER, matchedText, location});
        } else if (matchedText == ":") {
            tokens_.push_back({PreprocessorTokenType::COLON, matchedText, location});
        } else if (matchedText == "(") {
            tokens_.push_back({PreprocessorTokenType::OPEN_PARENTHESIS, matchedText, location});
        } else if (matchedText == ")") {
            tokens_.push_back({PreprocessorTokenType::CLOSE_PARENTHESIS, matchedText, location});
        } else if (matchedText == "[") {
            tokens_.push_back({PreprocessorTokenType::OPEN_BRACKET, matchedText, location});
        } else if (matchedText == "]") {
            tokens_.push_back({PreprocessorTokenType::CLOSE_BRACKET, matchedText, location});
        } else if (matchedText == "{") {
            tokens_.push_back({PreprocessorTokenType::OPEN_CURLY_BRACE, matchedText, location});
        } else if (matchedText == "}") {
            tokens_.push_back({PreprocessorTokenType::CLOSE_CURLY_BRACE, matchedText, location});
        } else if (matchedText == ",") {
            tokens_.push_back({PreprocessorTokenType::COMMA, matchedText, location});
        }
        if (!matchedText.empty()) {
            location = location.offsetByBytes(matchedText.size());
        }

        // Update the remaining text
        remainingText = match.suffix();
    }

    // Add any remaining normal text as a token
    if (!remainingText.empty()) {
        tokens_.push_back({PreprocessorTokenType::NORMAL, remainingText, location});
    }
}


std::string PreprocessorLine::toString() const {
    std::stringstream ss;
    ss
        << "=============================================" << std::endl
        << "PreprocessorLine: \"" << getLineWithoutWhitespace() << "\"" << std::endl
        << "FileLine " << getFileLocation().toString()
        << " Leading Whitespace: " << getLeadingWhitespace().size()
        << " Tokens: " << std::endl;

    using preprocessor::PreprocessorToken;
    using preprocessor::PreprocessorTokenType;
    // #PreprocessorTokenTypeNamesNeedToBeKeptInSync
    for (const PreprocessorToken& token : getTokens()) {
        switch (token.type) {
            case PreprocessorTokenType::SINGLE_LINE_COMMENT:
                ss << "  SINGLE_LINE_COMMENT: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::SEMICOLON:
                ss << "  SEMICOLON: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::BEGIN_MULTI_LINE_COMMENT:
                ss << "  BEGIN_MULTI_LINE_COMMENT: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::END_MULTI_LINE_COMMENT:
                ss << "  END_MULTI_LINE_COMMENT: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::QUOTED_STRING:
                ss << "  QUOTED_STRING: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::ESCAPED_CHARACTER:
                ss << "  ESCAPED_CHARACTER: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::MULTI_LINE_STRING:
                ss << "  MULTI_LINE_STRING: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::COLON:
                ss << "  COLON: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::OPEN_PARENTHESIS:
                ss << "  OPEN_PARENTHESIS: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::CLOSE_PARENTHESIS:
                ss << "  CLOSE_PARENTHESIS: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::OPEN_BRACKET:
                ss << "  OPEN_BRACKET: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::CLOSE_BRACKET:
                ss << "  CLOSE_BRACKET: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::OPEN_CURLY_BRACE:
                ss << "  OPEN_CURLY_BRACE: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::CLOSE_CURLY_BRACE:
                ss << "  CLOSE_CURLY_BRACE: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::COMMA:
                ss << "  COMMA: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::NORMAL:
                ss << "  NORMAL: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::COMMENT_OR_STRING_CONTENT:
                ss << "  COMMENT_OR_STRING_CONTENT: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::BEGIN_QUOTED_STRING:
                ss << "  BEGIN_QUOTED_STRING: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::END_QUOTED_STRING:
                ss << "  END_QUOTED_STRING: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::BEGIN_MULTI_LINE_STRING:
                ss << "  BEGIN_MULTI_LINE_STRING: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::END_MULTI_LINE_STRING:
                ss << "  END_MULTI_LINE_STRING: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::BEGIN_BLOCK:
                ss << "  BEGIN_BLOCK: " << token.text << std::endl;
                break;
            case PreprocessorTokenType::END_BLOCK:
                ss << "  END_BLOCK: " << token.text << std::endl;
                break;
            default:
                throw lexer::LexerException("oops");
        }
    }
    return ss.str();    
}

} // namespace preprocessor
} // namespace lexer
} // namespace yapllang
} // namespace org
