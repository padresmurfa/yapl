from transpiler.frontend.contexts.context import ContextBaseClass
from transpiler.frontend.contexts.identifier_declaration_context import IdentifierDeclarationContext
from transpiler.frontend.contexts.error_declaration_context import ErrorDeclarationContext

class CallableSegmentContext(ContextBaseClass):
    """
        A context-sensitive parser for parsing a callable-segment within a YAPL-class
    """

    def __init__(self, parent_class_context, indentation_level, siblings_by_name):
        """
            initializes the CallableSegmentContext

            'parent_class_context' is the ClassContext that contains this CallableSegmentContext
        """
        ContextBaseClass.__init__(self, None, parent_class_context, "CALLABLESEGMENT", indentation_level)
        self.__callable_segment_name = None
        self.__siblings_by_name = siblings_by_name

    def get_name(self):
        """
            retrieves the name of this context
        """
        return self.__callable_segment_name if self.__callable_segment_name is not None else "<unknown>"

    def __str__(self):
        return "YAPL frontend callable-segment context for callable-segment '{}'".format(self.get_fully_qualified_name())

    def process_line(self, lexer_line):
        """
            called by the framework to process a line
        """
        ContextBaseClass.push_lexer_line(self, lexer_line)
        leading_token = lexer_line.peek_leading_token()
        if leading_token.get_offset() == self.get_indentation_level():
            self.__process_line_callable_segment_statement_header(leading_token)
        elif leading_token.get_offset() == self.get_indentation_level() + 4:
            self.__process_line_callable_segment_body(leading_token)
        elif leading_token.is_empty_line():
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-CONTENT-AT-INDENT", "callable-segment declarations may only include direct content at indent level N+1", leading_token)

    def __process_line_callable_segment_statement_header(self, leading_token):
        """
            Helper function for process_line that handles the leading callable segment statement
        """
        if leading_token.is_callable_segment():
            self.__process_line_callable_segment_statement(leading_token)
        elif leading_token.is_comment():
            self.error("DID-NOT-EXPECT-PREFIX-COMMENT-FOR-CALLABLE-SEGMENT")
        elif leading_token.is_empty_line():
            self.trace("empty line statement encountered", leading_token)
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-CALLABLE-SEGMENT-STATEMENT-AT-OUTER-INDENT", "callable segments may only include the actual callable-segment-statement at indent one", leading_token)

    def __process_line_callable_segment_statement(self, callable_segment_name_token):
        """
            Helper function for process_line that handles the leading callable segment statement
        """
        self.trace("callable-segment declaration encountered", callable_segment_name_token)
        self.__callable_segment_name = callable_segment_name_token.get_lexeme_value()
        if self.__callable_segment_name in self.__siblings_by_name:
            self.error("EXPECTED-UNIQUE-CALLABLE-SEGMENT-NAME", "callable-segment statements must be unique. This callable segment has already been declared.", callable_segment_name_token)
        lexer_line = self.peek_lexer_line().consume(callable_segment_name_token)
        colon_token = lexer_line.peek_leading_token()
        if not colon_token.is_symbol(":"):
            self.error("EXPECTED-COLON-TERMINATOR-FOR-CALLABLE-SEGMENT-STATEMENT", "callable-segment statements must be terminated by a colon", colon_token)
        else:
            lexer_line = lexer_line.consume(colon_token)
            end_of_line = lexer_line.peek_leading_token()
            if end_of_line.is_end_of_line():
                pass
            elif end_of_line.is_comment():
                self.error("DIDNT-EXPECT-SUFFIX-COMMENT-FOR-CALLABLE-SEGMENT-STATEMENT", "callable-segment statements may not have suffix comments", end_of_line)
            else:
                self.error("DIDNT-EXPECT-JUNK-AFTER-CALLABLE-SEGMENT-STATEMENT", "callable-segment statements may not contain any additional code in the same line", end_of_line)
        ContextBaseClass.pop_lexer_line(self)

    def __process_line_callable_segment_body(self, leading_token):
        """
            Helper function for process_line that handles the leading callable segment statement
        """
        if self.__callable_segment_name in ("inputs", "returns", "emits"):
            # remove the identifier declaration statement and any optional prefix comment lines
            identifier_declaration_statement_line = self.pop_lexer_line()
            prefix_comment_lines = self.maybe_pop_prefix_comments_at_offset(self.get_indentation_level() + 4)
            # create the identifier-declaration context, attach it as a child of this context, and pass control to it
            identifier_declaration_context = IdentifierDeclarationContext(self, self.get_indentation_level() + 4)
            # forward the identifier-declaration statement and the prefix lines to the child context
            for prefix_comment_line in prefix_comment_lines:
                identifier_declaration_context.process_line(prefix_comment_line)
            identifier_declaration_context.process_line(identifier_declaration_statement_line)
            self.push_child_context(identifier_declaration_context)
        elif self.__callable_segment_name == "errors":
            # remove the error declaration statement and any optional prefix comment lines
            error_declaration_statement_line = self.pop_lexer_line()
            prefix_comment_lines = self.maybe_pop_prefix_comments_at_offset(self.get_indentation_level() + 4)
            # create the error-declaration context, attach it as a child of this context, and pass control to it
            error_declaration_context = IdentifierDeclarationContext(self, self.get_indentation_level() + 4)
            # forward the error-declaration statement and the prefix lines to the child context
            for prefix_comment_line in prefix_comment_lines:
                error_declaration_context.process_line(prefix_comment_line)
            error_declaration_context.process_line(error_declaration_statement_line)
            self.push_child_context(error_declaration_context)
        elif self.__callable_segment_name == "code":
            self.error("NOT-YET-IMPLEMENTED", "ignoring callable (type={}) segment body {}".format(self.__callable_segment_name, str(leading_token)), leading_token)
        elif self.__callable_segment_name == "preconditions":
            self.error("NOT-YET-IMPLEMENTED", "ignoring callable (type={}) segment body {}".format(self.__callable_segment_name, str(leading_token)), leading_token)
        elif self.__callable_segment_name == "postconditions":
            self.error("NOT-YET-IMPLEMENTED", "ignoring callable (type={}) segment body {}".format(self.__callable_segment_name, str(leading_token)), leading_token)
        else:
            self.error("NOT-IMPLEMENTED", "ignoring callable (type={}) segment body {}".format(self.__callable_segment_name, str(leading_token)), leading_token)
        ContextBaseClass.pop_lexer_line(self)

    def validate_contents(self):
        """
            called by the framework after processing the file, to validate the overall contents of the context
        """
        ContextBaseClass.validate_contents(self)
        if not self.get_content_callable_segment_name():
            self.error("CALLABLE-SEGMENT-MUST-HAVE-NAME", "a YAPL callable-segment must have a name", None)
        if not self.get_content_identifier_declarations():
            self.error("CALLABLE-SEGMENT-MUST-HAVE-CONTENT", "a YAPL callable-segment must have one or more content declarations", None)
        # TODO: sub-content

    def get_content_callable_segment_name(self):
        """
            Retrieves the name of this callable-segment, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__callable_segment_name

    def get_content_identifier_declarations(self):
        """
            retrieves the list of identifier declarations contained within this callable segment, which should non-empty for an input, returns or emits segment
        """
        identifier_declarations = []
        contents = self.get_contents()
        for content in contents:
            if isinstance(content, IdentifierDeclarationContext):
                identifier_declarations.append(content)
        return identifier_declarations

    def get_content_error_declarations(self):
        """
            retrieves the list of error declarations contained within this callable segment, which should be non-empty for an error declaration segment
        """
        error_declarations = []
        contents = self.get_contents()
        for content in contents:
            if isinstance(content, IdentifierDeclarationContext):
                error_declarations.append(content)
        return error_declarations
