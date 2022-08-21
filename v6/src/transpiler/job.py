import os

from transpiler.frontend.file_reader import FileReader as YAPLFileReader
from transpiler.frontend.contexts.context_stack import Stack as ContextStack
from transpiler.frontend.contexts.file_context import FileContext
from transpiler.frontend.lexer import Lexer as YAPLLexer, LexicallyAnalyzedLine
from transpiler.frontend.lexemes import Lexeme


class Job(object):

    def __init__(self):
        self.__input_file_name = None
        self.__output_directory_name = None
        self.__failed = False
        self.__context_stack = ContextStack()
        self.__verbose = False

    def get_context_stack(self):
        return self.__context_stack

    def failed(self):
        return self.__failed

    def set_verbose(self):
        self.__verbose = True

    def set_failed(self):
        self.__failed = True

    def get_input_file_name(self):
        return self.__input_file_name

    def set_input_file_name(self, file_name):
        self.__input_file_name = os.path.abspath(file_name)

    def get_output_directory_name(self):
        return self.__output_directory_name

    def set_output_directory_name(self, output_directory_name):
        self.__output_directory_name = os.path.abspath(output_directory_name)

    def run(self):
        input_file_name = self.get_input_file_name()
        reader = YAPLFileReader(input_file_name)
        initial_context = FileContext(self, input_file_name)
        self.__context_stack.push_context(initial_context)
        lexer = YAPLLexer()
        for line in reader.read_lines():
            lexer_line = lexer.analyze_line(line)
            leading_token = lexer_line.peek_leading_token()
            current_context = self.__context_stack.current_context()
            while (not self.__context_stack.is_empty()) and (not leading_token.is_empty_line()) and (leading_token.get_offset() < current_context.get_indentation_level()):
                current_context.process_end_of_context(lexer_line)
                current_context = current_context.pop_to_parent_context()
            if current_context is None:
                assert False, "did not expect to wind up in the root context"
            else:
                current_context.process_line(lexer_line)
            if self.failed():
                # TODO: consider recovering
                break
        if not self.failed():
            current_context = self.__context_stack.current_context()
            current_context.process_end_of_file()
            assert self.__context_stack.is_empty(), "expected the whole context stack to have been torn down during process-end-of-file"
        initial_context.validate_contents()

    def error(self, component, error_code, error_message, location, fully_qualified_name):
        self.set_failed()
        if location is None:
            print("ERROR: reported_by(component={}, error_code={}), location(file=\"{}\", name=\"{}\"), message={}".format(
                component, error_code, self.get_input_file_name(), fully_qualified_name, error_message
            ))
        elif isinstance(location, Lexeme):
            lexeme = location
            lexical_line = lexeme.get_lexical_line()
            print("ERROR: reported_by(component={}, error_code={}), location(file=\"{}\", line {}, offset={}, name=\"{}\"), lexeme={}, message={}".format(
                component, error_code, self.get_input_file_name(), lexical_line.get_line_number(), lexeme.get_offset(), fully_qualified_name, lexeme.get_printable_value(), error_message
            ))
        else:
            assert isinstance(location, LexicallyAnalyzedLine)
            lexical_line = location
            print("ERROR: reported_by(component={}, error_code={}), location(file=\"{}\", line {}, name=\"{}\"), message={}".format(
                component, error_code, self.get_input_file_name(), lexical_line.get_line_number(), fully_qualified_name, error_message
            ))

    def trace(self, component, trace_message, location, fully_qualified_name):
        if not self.__verbose:
            return
        if location is None:
            print("TRACE: reported_by(component={}), location(file=\"{}\", name=\"{}\"), message={}".format(
                component, self.get_input_file_name(), fully_qualified_name, trace_message
            ))
        elif isinstance(location, Lexeme):
            lexeme = location
            lexical_line = lexeme.get_lexical_line()
            print("TRACE: reported_by(component={}), location(file=\"{}\", line {}, offset={}, name=\"{}\"), lexeme={}, message={}".format(
                component, self.get_input_file_name(), lexical_line.get_line_number(), lexeme.get_offset(), fully_qualified_name, lexeme.get_printable_value(), trace_message
            ))
        else:
            assert isinstance(location, LexicallyAnalyzedLine)
            lexical_line = location
            print("TRACE: reported_by(component={}), location(file=\"{}\", line {}, name=\"{}\"), message={}".format(
                component, self.get_input_file_name(), lexical_line.get_line_number(), fully_qualified_name, trace_message
            ))
