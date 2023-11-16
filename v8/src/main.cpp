#include "include.hpp"
#include "lexer/file_reader/file_reader.hpp"
#include "lexer/tokenizer/tokenizer_lines.hpp"
#include "parser/parser_lines.hpp"

using namespace org::yapllang;

int main(int argc, char* argv[]) {
    try {
        if (argc != 2) {
            std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
            return -1;
        }

        std::string filename = argv[1];

/*
        std::cout << "--------------------------------------------------------" << std::endl;
        std::cout << " FILE READER" << std::endl;
        std::cout << "--------------------------------------------------------" << std::endl;
        */
        auto fileReader = lexer::file_reader::FileReader(filename);
        /*fileReader.print();
        std::cout << "--------------------------------------------------------" << std::endl;
        std::cout << std::endl;

        std::cout << "--------------------------------------------------------" << std::endl;
        std::cout << " TOKENIZER" << std::endl;
        std::cout << "--------------------------------------------------------" << std::endl;*/
        auto tokenizerLines = lexer::tokenizer::TokenizerLines::tokenize(fileReader.getLines());
/*        tokenizerLines.print();
        std::cout << "--------------------------------------------------------" << std::endl;
        std::cout << std::endl;

        std::cout << "--------------------------------------------------------" << std::endl;
        std::cout << " PARSER" << std::endl;
        std::cout << "--------------------------------------------------------" << std::endl;
        */
        auto parserLines = parser::ParserLines::parse(tokenizerLines);
        parserLines.print();
        std::cout << "--------------------------------------------------------" << std::endl;
        std::cout << std::endl;

    } catch (tools::Exception& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
        std::cerr << e.getStackTrace() << std::endl;
        return -1;
    } catch (std::runtime_error &e) {
        std::cerr << "std::runtime_error: " << e.what() << std::endl;
        return -1;
    } catch (std::exception& e) {
        std::cerr << "std::exception: " << e.what() << std::endl;
        return -1;
    }
    return 0;
}
