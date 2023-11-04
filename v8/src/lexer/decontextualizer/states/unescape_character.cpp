#include "handling_normal_stuff.hpp"
#include "../decontextualizer_exception.hpp"
#include "lexer/preprocessor/preprocessor.hpp"

namespace org {
namespace yapllang {
namespace lexer {
namespace decontextualizer {
namespace states {

// ##CharacterEscapesNeedToBeKeptInSync
// when character escape codes are added/removed, they must be kept in sync with our unescape function
std::string unescapeCharacter(const std::string &escapedCharacter, const lexer::preprocessor::PreprocessorToken &token) {
    // \"tnr\\bfv0a
    if (escapedCharacter.size() == 1) {
        switch (escapedCharacter[0]) {
            case '"':
                return "\"";
            case '\'':
                // not necessary in YAPL, but supported to increase compatibility with other programming languages
                return "'";
            case '?':
                // not necessary in YAPL, but supported to increase compatibility with other programming languages
                return "?";
            case 't':
                return "\t";
            case 'n':
                return "\n";
            case 'r':
                return "\r";
            case '\\':
                return "\\";
            case 'b':
                return "\b";
            case 'f':
                return "\f";
            case 'v':
                return "\v";
            case '0':
                // handled below as an octal escape
                break;
            case 'a':
                return "\a";
            case 'e':
                // compatibility with GCC: ESC character
                return "\x1B";
            default:
                break;
        }
    }
    std::smatch match;
    // octal escape code:
    //   \ + up to 3 octal digits
    if (std::regex_search(escapedCharacter, match, std::regex(R"([0-7]{1,3})"))) {
        int octalValue = std::stoi(escapedCharacter, 0, 8);
        char character = static_cast<char>(octalValue);
        return std::to_string(character);
    }
    // hexadecimal escape code:
    //   \x + any number of hex digits
    if (std::regex_search(escapedCharacter, match, std::regex(R"(x[0-9A-Fa-F]+)"))) {
        int hexValue = std::stoi(escapedCharacter.substr(1), 0, 16);
        char character = static_cast<char>(hexValue);
        return std::to_string(character);
    }
    // unicode escape code (4 hex):
    //   \u + 4 hex digits (Unicode BMP, new in C++11)
    if (std::regex_search(escapedCharacter, match, std::regex(R"(u[0-9A-Fa-F]{4})"))) {
        // Parse the hexadecimal string as an integer
        uint32_t unicodeValue;
        std::istringstream(escapedCharacter) >> std::hex >> unicodeValue;

        // Convert the integer to a wchar_t (Unicode character)
        char16_t unicodeChar = static_cast<char16_t>(unicodeValue);

        std::wstring wideStr = std::to_wstring(unicodeChar);

        // Create a std::wstring_convert object for UTF-8
        std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;

        // Convert the wide string to UTF-8 encoded string
        std::string utf8Str = converter.to_bytes(wideStr);
        return utf8Str;
    }

    /*

        TODO: add support for, or at very least raise unimplementedexception
        
while (std::regex_search(remainingText, match, std::regex(R"(|\\\\U[0-9A-Fa-F]{8}|\\[\"tnr\\bfva'\?]|:|\(|\)|\[|\]|\{|\}|\,))"))) {
        
        \U + 8 hex digits (Unicode astral planes, new in C++11)
        \0 = \00 = \000 = octal ecape for null character

    */
    throw UnknownEscapeCharacterException(token);
}

} // namespace states
} // namespace decontextualizer
} // namespace lexer
} // namespace yapllang
} // namespace org
