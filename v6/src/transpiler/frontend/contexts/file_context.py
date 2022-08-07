import os

from transpiler.frontend.contexts.context import ContextBaseClass
from transpiler.frontend.contexts.module_context import ModuleContext

class FileContext(ContextBaseClass):
    """
        A context-sensitive parser for parsing a YAPL file
    """

    def __init__(self, job, input_file_name):
        """
            initializer for FileContext.
            
            'job' is the job that this context is part of.
            'input_file_name' is the absolute filename that contains the YAPL file that this FileContext encapsulates
        """
        ContextBaseClass.__init__(self, job, None, "FILE")
        assert os.path.abspath(input_file_name) == input_file_name, "expected input_file_name to be an absolute file name"
        self.__input_file_name = input_file_name

    def __str__(self):
        return "YAPL frontend file context for file '{}'".format(self.__input_file_name)

    def process_line(self, lexer_line):
        """
            called by the framework to process a line
        """
        ContextBaseClass.push_lexer_line(self, lexer_line)
        leading_token = lexer_line.peek_leading_token()
        assert leading_token is not None, "expected a leading token here: {}".format(lexer_line)
        if leading_token.get_offset() != 0:
            # we don't a non-empty line in file-scope at any other offset than 0
            self.error("FILE-SCOPED-CONTENTS-MUST-RESIDE-AT-INDENT-ZERO", "file-scoped contents must reside at indentation-level zero",  leading_token)
        elif leading_token.is_keyword("module"):
            self.trace("module statement encountered", leading_token)
            self.__process_line_containing_module_statement(leading_token)
        elif leading_token.is_comment():
            self.trace("comment statement encountered", leading_token)
        elif leading_token.is_empty_line():
            self.trace("empty line encountered", leading_token)
        else:
            self.error("FILE-SCOPED-CONTENTS-UNEXPECTED-TOKEN", "file-scoped contents may only be comments, empty lines, and module declarations",  leading_token)

    def __process_line_containing_module_statement(self, leading_token):
        """
            helper function for process_line, which handles lines that contain a module statement

            Removes the module statement line and the prefix comment lines from the unprocessed contents, and
            forwards them to a ModuleContext object that is created as a child of this object.
        """
        # remove the module statement and any optional prefix comment lines
        module_statement_line = self.pop_lexer_line()
        prefix_comment_lines = self.maybe_pop_prefix_comments_at_offset(0)
        # create the module context, attach it as a child of this context, and pass control to it
        module_context = ModuleContext(self)
        # forward the module statement and the prefix lines to the module context
        for prefix_comment_line in prefix_comment_lines:
            module_context.process_line(prefix_comment_line)
        module_context.process_line(module_statement_line)
        self.push_child_context(module_context)

    def process_end_of_file(self):
        """
            called by the framework on the current Context when the end-of-file is reached. The Context should pop itself from the stack,
            and forward the process_end_of_file call to its parent context, if any.
        """
        parent = self.pop_to_parent_context()
        assert parent is None

    def validate_contents(self):
        """
            called by the framework after processing the file, to validate the overall contents of the context
        """
        ContextBaseClass.validate_contents(self)
        if not self.get_content_modules():
            self.error("FILE-MUST-CONTAIN-AT-LEAST-ONE-MODULE", "a YAPL file most content at least one module", None)

    def get_content_absolute_file_name(self):
        """
            retrieves the absolute file name of this FileContext, which is part of it's value in the abstract syntax tree
        """
        return self.__input_file_name

    def get_content_modules(self):
        """
            retrieves the list of modules contained within this FileContext, which should be > 0 for a valid YAPL file
        """
        modules = []
        contents = self.get_contents()
        for content in contents:
            if isinstance(content, ModuleContext):
                modules.append(content)
        return modules
