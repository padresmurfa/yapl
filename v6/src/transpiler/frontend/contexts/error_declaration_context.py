from transpiler.frontend.contexts.context import ContextBaseClass

class ErrorDeclarationContext(ContextBaseClass):
    """
        A context-sensitive parser for parsing a error-declaration within a YAPL-class
    """

    def __init__(self, parent_class_context, indentation_level):
        """
            initializes the ErrorDeclarationContext

            'parent_class_context' is the ClassContext that contains this ErrorDeclarationContext
        """
        ContextBaseClass.__init__(self, None, parent_class_context, "ERRORDECLARATION", indentation_level)
        self.__error_name = None
        self.__prefix_comments = []
        self.__suffix_comment = ""

    def get_name(self):
        """
            retrieves the name of this context
        """
        return self.__error_name if self.__error_name is not None else "<unknown>"

    def __str__(self):
        return "YAPL frontend error-declaration context for error-declaration '{}'".format(self.get_fully_qualified_name())

    def process_line(self, lexer_line):
        """
            called by the framework to process a line
        """
        ContextBaseClass.push_lexer_line(self, lexer_line)
        leading_token = lexer_line.peek_leading_token()
        if leading_token.get_offset() == self.get_indentation_level():
            self.__process_line_error_statement(leading_token)
        elif leading_token.is_empty_line():
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-CONTENT-AT-INDENT", "error-declaration declarations may only include direct content at indent level N", leading_token)

    def __process_line_error_statement(self, leading_token):
        """
            Helper function for process_line that handles the leading error declaration statement
        """
        if leading_token.is_identifier():
            self.__process_line_error_declaration_statement(leading_token)
        elif leading_token.is_comment():
            self.trace("prefix comment statement encountered", leading_token)
            self.__prefix_comments.append(leading_token.get_lexeme_value())
            ContextBaseClass.pop_lexer_line(self)
        elif leading_token.is_empty_line():
            self.trace("empty line statement encountered", leading_token)
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-ERROR-DECLARATION-STATEMENT", "error declarations may only include the actual error-declaration-statement", leading_token)

    def __process_line_error_declaration_statement(self, error_name_token):
        """
            Helper function for process_line that handles the leading error declaration statement
        """
        self.trace("error-declaration-statement encountered", error_name_token)
        self.__error_name = error_name_token.get_lexeme_value()
        lexer_line = self.peek_lexer_line().consume(error_name_token)
        # now there might be an optional suffix comment
        suffix_comment = lexer_line.peek_leading_token()
        if suffix_comment.is_end_of_line():
            pass
        elif suffix_comment.is_comment_horizontal_rule():
            self.error("EXPECTED-SUFFIX-COMMENT-FOR-ERROR-DECLARATION-NOT-HORIZONTAL-RULE", "error declaration statements may have suffix comments, but a horizontal rule may not be used as a suffix comment", suffix_comment)
        elif suffix_comment.is_comment():
            self.__suffix_comment = suffix_comment.get_lexeme_value()
        else:
            self.error("EXPECTED-SUFFIX-COMMENT-FOR-ERROR-DECLARATION", "error declaration statements may only be followed by suffix comments in the same line", suffix_comment)
        ContextBaseClass.pop_lexer_line(self)

    def validate_contents(self):
        """
            called by the framework after processing the file, to validate the overall contents of the context
        """
        ContextBaseClass.validate_contents(self)
        if not self.get_content_error_name():
            self.error("ERROR-DECLARATION-MUST-HAVE-NAME", "a YAPL error-declaration must have a name", None)
        if not (self.get_content_error_prefix_comments() or self.get_content_error_suffix_comment()):
            self.error("ERROR-MUST-BE-COMMENTED", "a YAPL error must be commented, either using prefix- or suffix-notation", None)

    def get_content_error_name(self):
        """
            Retrieves the name of this error-declaration, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__error_name

    def get_content_error_prefix_comments(self):
        """
            Retrieves the prefix-comments of this error, as they shall be exposed to the abstract-syntax-tree
        """
        return self.__prefix_comments

    def get_content_error_suffix_comment(self):
        """
            Retrieves the suffix-comment of this error, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__suffix_comment
