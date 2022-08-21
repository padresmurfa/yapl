from transpiler.frontend.contexts.context import ContextBaseClass
from transpiler.frontend.contexts.class_context import ClassContext

class ModuleContext(ContextBaseClass):
    """
        A context-sensitive parser for handling a YAPL module
    """

    def __init__(self, parent_file_context, indentation_level):
        """
            initializies the parser

            'parent_file_context' is the parent FileContext object that this ModuleContext resides within.
        """
        ContextBaseClass.__init__(self, None, parent_file_context, "MODULE", indentation_level=indentation_level)
        self.__module_fully_qualified_name = None
        self.__prefix_comments = []
        self.__suffix_comment = ""

    def get_fully_qualified_name(self):
        """
            retrieves the fully-qualified name of this context
        """
        return self.__module_fully_qualified_name if self.__module_fully_qualified_name is not None else "<unknown>"

    def get_name(self):
        """
            retrieves the name of this module, which is the last token in its fully-qualified name
        """
        return self.get_fully_qualified_name().split(".")[-1]

    def __str__(self):
        return "YAPL frontend module context for module '{}'".format(self.get_fully_qualified_name())

    def process_line(self, lexer_line):
        """
            called by the framework to process a line
        """
        ContextBaseClass.push_lexer_line(self, lexer_line)
        leading_token = lexer_line.peek_leading_token()
        if leading_token.get_offset() == self.get_indentation_level():
            self.__process_module_statement_line(leading_token)
        elif leading_token.get_offset() == self.get_indentation_level() + 4:
            self.__process_module_body_line(leading_token)
        else:
            self.error("EXPECTED-CONTENT-AT-INDENT-ONE", "module declarations may only include direct content at indent level one (offset: 4 characters)", leading_token)

    def __process_module_body_line(self, leading_token):
        """
            Helper function to handle the inner content of the ModuleContext
        """
        if leading_token.is_keyword("class"):
            self.__process_module_body_line_containing_class_statement(leading_token)
        elif leading_token.is_comment():
            # assuming that this is a class-comment
            pass
        else:
            self.error("NOT-IMPLEMENTED", "ignoring module content", leading_token)

    def __process_module_body_line_containing_class_statement(self, leading_token):
        """
            helper function for process_line, which handles lines that contain a class statement

            Removes the class statement line and the prefix comment lines from the unprocessed contents, and
            forwards them to a ClassContext object that is created as a child of this object.
        """
        self.trace("class statement encountered", leading_token)
        # remove the class statement and any optional prefix comment lines
        class_statement_line = self.pop_lexer_line()
        prefix_comment_lines = self.maybe_pop_prefix_comments_at_offset(self.get_indentation_level() + 4)
        # create the class context, attach it as a child of this context, and pass control to it
        class_context = ClassContext(self, self.get_indentation_level() + 4)
        # forward the class statement and the prefix lines to the class context
        for prefix_comment_line in prefix_comment_lines:
            class_context.process_line(prefix_comment_line)
        class_context.process_line(class_statement_line)
        self.push_child_context(class_context)

    def __process_module_statement_line(self, leading_token):
        """
            Helper function to handle the whole module-statement at indent-zero
        """
        # prefix comment and module statement happen at indent 0
        if leading_token.is_keyword("module"):
            self.__process_module_statement_line_containing_module_statement(leading_token)
        elif leading_token.is_comment():
            self.__process_module_statement_line_containing_prefix_comment(leading_token)
        elif leading_token.is_empty_line():
            self.trace("empty line statement encountered", leading_token)
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-PREFIX-COMMENT-OR-MODULE-STATEMENT-AT-INDENT-ZERO", "module declarations may only include prefix-comments and the actual module-statement at indent zero", leading_token)

    def __process_module_statement_line_containing_prefix_comment(self, leading_token):
        """
            Helper function for process_line to handle the prefix comment for the module statement 

            1. appends the prefix comment to __prefix_comments
            2. removes the line from the ModuleContext's unprocessed contents
        """
        self.trace("prefix comment statement encountered", leading_token)
        self.__prefix_comments.append(leading_token.get_lexeme_value())
        ContextBaseClass.pop_lexer_line(self)

    def __process_module_statement_line_containing_module_statement(self, leading_token):
        """
            Helper function for process_line to handle the initial module statement.

            1. populates the member variables __module_fully_qualified_name and __suffix_comment
            2. removes the line from the ModuleContext's unprocessed contents
        """
        self.trace("module statement encountered", leading_token)
        lexer_line = self.peek_lexer_line().consume(leading_token)
        module_name = lexer_line.peek_leading_token()
        if not module_name.is_qualified_identifier():
            self.error("EXPECTED-QUALIFIED-NAME", "modules must have fully qualified names", module_name)
        elif not module_name.is_valid_fully_qualified_token():
            self.error("EXPECTED-VALID-FULLY-QUALIFIED-NAME", "modules must have VALID fully qualified names. A valid fully-qualified module name must consist of at least three dot-separated valid tokens.", module_name)
        else:
            self.__module_fully_qualified_name = module_name.get_lexeme_value()
            self.trace("module fully qualified name: {}".format(self.__module_fully_qualified_name), module_name)
            lexer_line = lexer_line.consume(module_name)
            colon_token = lexer_line.peek_leading_token()
            if not colon_token.is_symbol(":"):
                self.error("EXPECTED-COLON-TERMINATOR-FOR-MODULE-STATEMENT", "module statements must be terminated by a colon", colon_token)
            else:
                lexer_line = lexer_line.consume(colon_token)
                # now there might be an optional suffix comment
                suffix_comment = lexer_line.peek_leading_token()
                if suffix_comment.is_end_of_line():
                    pass
                elif suffix_comment.is_comment_horizontal_rule():
                    self.error("EXPECTED-SUFFIX-COMMENT-FOR-MODULE-STATEMENT-NOT-HORIZONTAL-RULE", "module statements may have suffix comments, but a horizontal rule may not be used as a suffix comment", suffix_comment)
                elif suffix_comment.is_comment():
                    self.__suffix_comment = suffix_comment.get_lexeme_value()
                else:
                    self.error("EXPECTED-SUFFIX-COMMENT-FOR-MODULE-STATEMENT", "module statements may only be followed by suffix comments in the same line", suffix_comment)
        ContextBaseClass.pop_lexer_line(self)

    def validate_contents(self):
        ContextBaseClass.validate_contents(self)
        if not (self.get_content_module_prefix_comments() or self.get_content_module_suffix_comment()):
            self.error("MODULE-MUST-BE-COMMENTED", "a YAPL module must be commented, either using prefix- or suffix-notation", None)
        if not self.get_content_module_fully_qualified_name():
            self.error("MODULE-MUST-HAVE-NAME", "a YAPL module must have a fully qualified name", None)
        if not self.get_content_classes():
            self.error("MODULE-MUST-HAVE-CONTENTS", "a YAPL module must contain at least one class, function, type or constant", None)

    def get_content_classes(self):
        classes = []
        contents = self.get_contents()
        for content in contents:
            if isinstance(content, ClassContext):
                classes.append(content)
        return classes

    def get_content_module_fully_qualified_name(self):
        return self.__module_fully_qualified_name

    def get_content_module_prefix_comments(self):
        return self.__prefix_comments

    def get_content_module_suffix_comment(self):
        return self.__suffix_comment
