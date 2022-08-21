from transpiler.frontend.contexts.context import ContextBaseClass
from transpiler.frontend.contexts.callable_segment_context import CallableSegmentContext

class CallableContext(ContextBaseClass):
    """
        A context-sensitive parser for parsing a YAPL callable, be it a method, function, or generator
    """

    def __init__(self, parent_context, indentation_level):
        """
            initializes the CallableContext

            'parent_context' is the Context that contains this CallableContext
        """
        ContextBaseClass.__init__(self, None, parent_context, "CALLABLE", indentation_level)
        self.__callable_type = None
        self.__callable_name = None
        self.__prefix_comments = []
        self.__suffix_comment = ""

    def get_name(self):
        """
            retrieves the name of this context
        """
        if self.__callable_type == "constructor":
            return self.__callable_type
        else:
            return self.__callable_name if self.__callable_name is not None else "<unknown>"

    def __str__(self):
        return "YAPL frontend context for callable '{}'".format(self.get_fully_qualified_name())

    def process_line(self, lexer_line):
        """
            called by the framework to process a line
        """
        ContextBaseClass.push_lexer_line(self, lexer_line)
        leading_token = lexer_line.peek_leading_token()
        if leading_token.get_offset() == self.get_indentation_level():
            self.__process_line_callable_statement_header(leading_token)
        elif leading_token.get_offset() == self.get_indentation_level() + 4:
            self.__process_line_callable_body(leading_token)
        elif leading_token.is_empty_line():
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-CONTENT-AT-SPECIFIC-INDENT", "callables may only be located at the indent level they are declared on plus one indent level for callable-facets", leading_token)

    def __process_line_callable_statement_header(self, leading_token):
        """
            Helper function for process_line that handles the leading callable declaration statement
        """
        if leading_token.is_callable():
            self.__process_line_callable_statement(leading_token)
        elif leading_token.is_comment():
            self.trace("prefix comment statement encountered", leading_token)
            self.__prefix_comments.append(leading_token.get_lexeme_value())
            ContextBaseClass.pop_lexer_line(self)
        elif leading_token.is_empty_line():
            self.trace("empty line statement encountered", leading_token)
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-PREFIX-COMMENT-OR-CALLABLE-STATEMENT-AT-RELATIVE-INDENT-ZERO", "callable declarations may only include prefix-comments and the actual callable-statement at relative indent zero", leading_token)

    def __process_line_callable_statement(self, leading_token):
        """
            Helper function for process_line that handles the leading callable declaration statement
        """
        self.trace("callable statement encountered", leading_token)
        self.__callable_type = leading_token.get_lexeme_value()
        lexer_line = self.peek_lexer_line().consume(leading_token)
        callable_name = lexer_line.peek_leading_token()
        if not callable_name.is_identifier():
            self.error("EXPECTED-IDENTIFIER", "callables must have a name", callable_name)
        elif not callable_name.is_valid_identifier():
            self.error("EXPECTED-VALID-IDENTIFIER", "callable names must be valid identifiers", callable_name)
        else:
            self.__callable_name = callable_name.get_lexeme_value()
            self.trace("callable name: {}".format(self.__callable_name), callable_name)
            lexer_line = lexer_line.consume(callable_name)
            colon_token = lexer_line.peek_leading_token()
            if not colon_token.is_symbol(":"):
                self.error("EXPECTED-COLON-TERMINATOR-FOR-CALLABLE-STATEMENT", "callable statements must be terminated by a colon", colon_token)
            else:
                lexer_line = lexer_line.consume(colon_token)
                # now there might be an optional suffix comment
                suffix_comment = lexer_line.peek_leading_token()
                if suffix_comment.is_end_of_line():
                    pass
                elif suffix_comment.is_comment_horizontal_rule():
                    self.error("EXPECTED-SUFFIX-COMMENT-FOR-CALLABLE-STATEMENT-NOT-HORIZONTAL-RULE", "callable statements may have suffix comments, but a horizontal rule may not be used as a suffix comment", suffix_comment)
                elif suffix_comment.is_comment():
                    self.__suffix_comment = suffix_comment.get_lexeme_value()
                else:
                    self.error("EXPECTED-SUFFIX-COMMENT-FOR-CALLABLE-STATEMENT", "callable statements may only be followed by suffix comments in the same line", suffix_comment)
        ContextBaseClass.pop_lexer_line(self)

    def __process_line_callable_body(self, leading_token):
        """
            Helper function for process_line that handles the callable's body'
        """
        if leading_token.is_callable_segment():
            self.__process_line_callable_segment_statement()
        else:
            self.trace("ignoring callable-segment content", leading_token)

    def __process_line_callable_segment_statement(self):
        """
            helper function for process_line, which handles lines that contain a callable-segment statement

            Removes the callable-segment statement line and the prefix comment lines from the unprocessed contents, and
            forwards them to a CallableSegmentContext object that is created as a child of this object.
        """
        # remove the callable-segment statement and any optional prefix comment lines
        callable_segment_statement_line = self.pop_lexer_line()
        prefix_comment_lines = self.maybe_pop_prefix_comments_at_offset(self.get_indentation_level() + 4)
        # create the callable-segment-context, attach it as a child of this context, and pass control to it
        siblings_by_name = {}
        siblings = self.get_contents()
        for sibling in siblings:
            if isinstance(sibling, CallableSegmentContext):
                siblings_by_name[sibling.get_callable_segment_name()] = sibling
        callable_segment_context = CallableSegmentContext(self, self.get_indentation_level() + 4, siblings_by_name)
        # forward the callable-segment statement and the prefix lines to the callable-segment-context
        for prefix_comment_line in prefix_comment_lines:
            callable_segment_context.process_line(prefix_comment_line)
        callable_segment_context.process_line(callable_segment_statement_line)
        self.push_child_context(callable_segment_context)

    def validate_contents(self):
        """
            called by the framework after processing the file, to validate the overall contents of the context
        """
        ContextBaseClass.validate_contents(self)
        if not (self.get_content_callable_prefix_comments() or self.get_content_callable_suffix_comment()):
            self.error("CALLABLE-MUST-BE-COMMENTED", "a YAPL callable must be commented, either using prefix- or suffix-notation", None)
        if not self.get_content_callable_type():
            self.error("CALLABLE-MUST-HAVE-TYPE", "a YAPL callable must have a callable type", None)
        if not self.get_content_callable_name():
            self.error("CALLABLE-MUST-HAVE-NAME", "a YAPL callable must have a callable name", None)

    def get_content_callable_type(self):
        """
            Retrieves the callable-type of this context, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__callable_type

    def get_content_callable_name(self):
        """
            Retrieves the callable-name of this context, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__callable_name

    def get_content_callable_prefix_comments(self):
        """
            Retrieves the prefix-comments of this callable-context, as they shall be exposed to the abstract-syntax-tree
        """
        return self.__prefix_comments

    def get_content_callable_suffix_comment(self):
        """
            Retrieves the suffix-comment of this callable-context, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__suffix_comment

    def get_content_callable_segments(self):
        """
            Retrieves the callable-segments of this callable-context, as they shall be exposted to the abstract-syntax-tree
        """
        callable_segments = {}
        contents = self.get_contents()
        for content in contents:
            if isinstance(content, CallableSegmentContext):
                callable_segments[content.get_callable_segment_name()] = content
        return callable_segments