from transpiler.frontend.contexts.context import ContextBaseClass

class ClassContext(ContextBaseClass):
    """
        A context-sensitive parser for parsing a class within a YAPL file
    """

    def __init__(self, parent_module_context):
        """
            initializes the ClassContext

            'parent_module_context' is the ModuleContext that contains this ClassContext
        """
        ContextBaseClass.__init__(self, None, parent_module_context, "CLASS")
        self.__class_name = None
        self.__prefix_comments = []
        self.__suffix_comment = ""

    def get_debug_class_fully_qualified_name(self):
        """
            returns a debug-suitable version of this class's fully-qualified name, including the fully-qualified name of the module
            that contains it
        """
        module_fully_qualified_name = self.get_parent_context().get_debug_module_fully_qualified_name()
        class_name = self.get_debug_class_name()
        return module_fully_qualified_name + "." + class_name

    def get_debug_class_name(self):
        """
            returns a debug-suitable version of this class's name.
        """
        return self.__class_name if self.__class_name is not None else "<unknown>"

    def __str__(self):
        return "YAPL frontend class context for class '{}'".format(self.get_debug_class_fully_qualified_name())

    def process_line(self, lexer_line):
        """
            called by the framework to process a line
        """
        ContextBaseClass.push_lexer_line(self, lexer_line)
        leading_token = lexer_line.peek_leading_token()
        if leading_token.get_offset() == 4:
            self.__process_line_class_statement_header(leading_token)
        elif leading_token.get_offset() == 8:
            self.__process_line_class_body(leading_token)
        else:
            self.error("EXPECTED-CONTENT-AT-INDENT-TWO", "class declarations may only include direct content at indent level two (offset: 8 characters)", leading_token)

    def __process_line_class_statement_header(self, leading_token):
        """
            Helper function for process_line that handles the leading class declaration statement
        """
        # prefix comment and class statement happen at indent 4
        if leading_token.is_keyword("class"):
            self.__process_line_class_statement(leading_token)
        elif leading_token.is_comment():
            self.trace("prefix comment statement encountered", leading_token)
            self.__prefix_comments.append(leading_token.get_lexeme_value())
            ContextBaseClass.pop_lexer_line(self)
        elif leading_token.is_empty_line():
            self.trace("empty line statement encountered", leading_token)
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-PREFIX-COMMENT-OR-CLASS-STATEMENT-AT-INDENT-ONE", "class declarations may only include prefix-comments and the actual class-statement at indent one", leading_token)

    def __process_line_class_statement(self, leading_token):
        """
            Helper function for process_line that handles the leading class declaration statement
        """
        # prefix comment and class statement happen at indent 4
        self.trace("class statement encountered", leading_token)
        lexer_line = self.peek_lexer_line().consume(leading_token)
        class_name = lexer_line.peek_leading_token()
        if not class_name.is_token():
            self.error("EXPECTED-TOKEN", "classes must have a name", class_name)
        elif not class_name.is_valid_token():
            self.error("EXPECTED-VALID-TOKEN", "class names must be valid tokens", class_name)
        else:
            self.__class_name = class_name.get_lexeme_value()
            self.trace("class name: {}".format(self.__class_name), class_name)
            lexer_line = lexer_line.consume(class_name)
            # TODO - extends X, implements Y, aggregates Z, ...
            colon_token = lexer_line.peek_leading_token()
            if not colon_token.is_symbol(":"):
                self.error("EXPECTED-COLON-TERMINATOR-FOR-CLASS-STATEMENT", "class statements must be terminated by a colon", colon_token)
            else:
                lexer_line = lexer_line.consume(colon_token)
                # now there might be an optional suffix comment
                suffix_comment = lexer_line.peek_leading_token()
                if suffix_comment.is_end_of_line():
                    pass
                elif suffix_comment.is_comment_horizontal_rule():
                    self.error("EXPECTED-SUFFIX-COMMENT-FOR-CLASS-STATEMENT-NOT-HORIZONTAL-RULE", "class statements may have suffix comments, but a horizontal rule may not be used as a suffix comment", suffix_comment)
                elif suffix_comment.is_comment():
                    self.__suffix_comment = suffix_comment.get_lexeme_value()
                else:
                    self.error("EXPECTED-SUFFIX-COMMENT-FOR-CLASS-STATEMENT", "class statements may only be followed by suffix comments in the same line", suffix_comment)
        ContextBaseClass.pop_lexer_line(self)

    def __process_line_class_body(self, leading_token):
        """
            Helper function for process_line that handles the leading class declaration statement
        """
        self.trace("ignoring class content", lexer_line)
        # TODO: class facets


    def process_end_of_file(self):
        """
            called by the framework on the current Context when the end-of-file is reached. The Context should pop itself from the stack,
            and forward the process_end_of_file call to its parent context, if any.
        """
        self.pop_to_parent_context().process_end_of_file()
        
    def validate_contents(self):
        """
            called by the framework after processing the file, to validate the overall contents of the context
        """
        ContextBaseClass.validate_contents(self)
        if not (self.get_content_class_prefix_comments() or self.get_content_class_suffix_comment()):
            self.error("CLASS-MUST-BE-COMMENTED", "a YAPL class must be commented, either using prefix- or suffix-notation", None)

    def get_content_class_name(self):
        """
            Retrieves the class-name of this ClassContext, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__class_name

    def get_content_class_prefix_comments(self):
        """
            Retrieves the prefix-comments of this ClassContext, as they shall be exposed to the abstract-syntax-tree
        """
        return self.__prefix_comments

    def get_content_class_suffix_comment(self):
        """
            Retrieves the suffix-comment of this ClassContext, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__suffix_comment

