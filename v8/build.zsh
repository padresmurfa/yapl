#!/bin/zsh

#    -I /opt/homebrew/Cellar/utf8cpp/4.0.1/include \

# sticking with C++11, since the codecvt family is deprecated in C++17 and no alternative was provided
/usr/bin/clang++ \
    -fcolor-diagnostics -fansi-escape-codes \
    -std=c++11 \
    -I ./include \
    -I ./src \
    -g ./src/main.cpp \
    -g ./src/lexer/lexer_exception.cpp \
    -g ./src/parser/states/parser_context.cpp \
    -g ./src/parser/states/parser_states.cpp \
    -g ./src/parser/states/handle_begin_of_line.cpp \
    -g ./src/parser/states/handling_brackets.cpp \
    -g ./src/parser/states/handling_curly_braces.cpp \
    -g ./src/parser/states/handling_indented_block.cpp \
    -g ./src/parser/states/handling_multi_line_string.cpp \
    -g ./src/parser/states/handling_normal_stuff.cpp \
    -g ./src/parser/states/handling_parenthesis.cpp \
    -g ./src/parser/states/handling_quoted_string.cpp \
    -g ./src/parser/states/handling_single_line_comment.cpp \
    -g ./src/parser/states/unescape_character.cpp \
    -g ./src/parser/parser_exception.cpp \
    -g ./src/parser/parser_line.cpp \
    -g ./src/parser/parser_lines.cpp \
    -g ./src/parser/parser.cpp \
    -g ./src/lexer/file_reader/file_line.cpp \
    -g ./src/lexer/file_reader/file_lines.cpp \
    -g ./src/lexer/file_reader/file_location.cpp \
    -g ./src/lexer/file_reader/file_reader_exception.cpp \
    -g ./src/lexer/file_reader/file_reader.cpp \
    -g ./src/lexer/file_reader/file.cpp \
    -g ./src/lexer/tokenizer/tokenizer.cpp \
    -g ./src/lexer/tokenizer/tokenizer_line.cpp \
    -g ./src/lexer/tokenizer/tokenizer_lines.cpp \
    -g ./src/tools/exception.cpp \
    -g ./src/tools/stacktrace.cpp \
    -o ./bin/yaplparser
