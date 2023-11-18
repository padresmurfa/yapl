CC = clang++
CFLAGS = -std=c++11 -I ./include -I ./src -fcolor-diagnostics -fansi-escape-codes
LDFLAGS =

# Source files
SRCS = \
        src/main.cpp \
        src/lexer/lexer_exception.cpp \
        src/parser/states/parser_context.cpp \
        src/parser/states/parser_states.cpp \
        src/parser/states/handle_begin_of_line.cpp \
        src/parser/states/handle_end_of_file.cpp \
        src/parser/states/handle_end_of_line.cpp \
        src/parser/states/handling_brackets.cpp \
        src/parser/states/handling_curly_braces.cpp \
        src/parser/states/handling_indented_block.cpp \
        src/parser/states/handling_multi_line_string.cpp \
        src/parser/states/handling_normal_stuff.cpp \
        src/parser/states/handling_parenthesis.cpp \
        src/parser/states/handling_quoted_string.cpp \
        src/parser/states/handling_multi_line_comment.cpp \
        src/parser/states/handling_single_line_comment.cpp \
        src/parser/states/unescape_character.cpp \
        src/parser/parser_exception.cpp \
        src/parser/parser_line.cpp \
        src/parser/parser_lines.cpp \
        src/parser/parser.cpp \
        src/lexer/file_reader/file_line.cpp \
        src/lexer/file_reader/file_lines.cpp \
        src/lexer/file_reader/file_location.cpp \
        src/lexer/file_reader/file_reader_exception.cpp \
        src/lexer/file_reader/file_reader.cpp \
        src/lexer/file_reader/file.cpp \
        src/lexer/tokenizer/tokenizer.cpp \
        src/lexer/tokenizer/tokenizer_line.cpp \
        src/lexer/tokenizer/tokenizer_lines.cpp \
        src/tools/exception.cpp \
        src/tools/stacktrace.cpp

# Create a list of source file directories
SRCDIRS = $(sort $(dir $(SRCS)))

# Output executable name
TARGET = ./bin/yaplparser

# Output directory for object files
OBJDIR = obj

# Object files (automatically generated with directory structure)
OBJS = $(patsubst %.cpp,$(OBJDIR)/%.o,$(SRCS))

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $(TARGET) $(OBJS)

# Rule to create the object directory and subdirectories if they don't exist
$(OBJDIR):
	mkdir -p $(OBJDIR) $(addprefix $(OBJDIR)/,$(SRCDIRS))

$(OBJDIR)/%.o: %.cpp | $(OBJDIR)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
