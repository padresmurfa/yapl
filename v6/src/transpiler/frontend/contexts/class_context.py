from transpiler.frontend.contexts.context import ContextBaseClass
from transpiler.frontend.contexts.class_facet_context import ClassFacetContext

class ClassContext(ContextBaseClass):
    """
        A context-sensitive parser for parsing a class within a YAPL-module
    """

    def __init__(self, parent_module_context, indentation_level):
        """
            initializes the ClassContext

            'parent_module_context' is the ModuleContext that contains this ClassContext
        """
        ContextBaseClass.__init__(self, None, parent_module_context, "CLASS", indentation_level)
        self.__class_name = None
        self.__prefix_comments = []
        self.__suffix_comment = ""

    def get_name(self):
        """
            retrieves the name of this context
        """
        return self.__class_name if self.__class_name is not None else "<unknown>"

    def __str__(self):
        return "YAPL frontend class context for class '{}'".format(self.get_fully_qualified_name())

    def process_line(self, lexer_line):
        """
            called by the framework to process a line
        """
        ContextBaseClass.push_lexer_line(self, lexer_line)
        leading_token = lexer_line.peek_leading_token()
        if leading_token.get_offset() == self.get_indentation_level():
            self.__process_line_class_statement_header(leading_token)
        elif leading_token.get_offset() == self.get_indentation_level() + 4:
            self.__process_line_class_body(leading_token)
        elif leading_token.is_empty_line():
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-CONTENT-AT-INDENT-TWO", "class declarations may only include direct content at indent level two (offset: 8 characters)", leading_token)

    def __process_line_class_statement_header(self, leading_token):
        """
            Helper function for process_line that handles the leading class declaration statement
        """
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
        self.trace("class statement encountered", leading_token)
        lexer_line = self.peek_lexer_line().consume(leading_token)
        class_name = lexer_line.peek_leading_token()
        if not class_name.is_identifier():
            self.error("EXPECTED-IDENTIFIER", "classes must have a name", class_name)
        elif not class_name.is_valid_identifier():
            self.error("EXPECTED-VALID-IDENTIFIER", "class names must be valid identifiers", class_name)
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
            Helper function for process_line that handles the class's body
        """
        if leading_token.is_visibility_level():
            class_facet_type_keyword = self.peek_lexer_line().clone().consume(leading_token).peek_leading_token()
            if class_facet_type_keyword.is_class_facet_type():
                self.__process_line_class_body_facet_statement()
            else:
                self.error("EXPECTED-FACET-KEYWORD", "class-facet statements should start with a visibility-level, followed by the facet keyword", facet_keyword)
        else:
            self.error("UNEXPECTED-CLASS-CONTENT", "YAPL classes may only contain class-facet statements", leading_token)

    def __process_line_class_body_facet_statement(self):
        """
            helper function for process_line, which handles lines that contain a class-facet statement

            Removes the class-facet statement line and the prefix comment lines from the unprocessed contents, and
            forwards them to a ClassFacetContext object that is created as a child of this object.
        """
        # remove the class statement and any optional prefix comment lines
        class_facet_statement_line = self.pop_lexer_line()
        prefix_comment_lines = self.maybe_pop_prefix_comments_at_offset(self.get_indentation_level() + 4)
        # create the class context, attach it as a child of this context, and pass control to it
        class_facet_context = ClassFacetContext(self, self.get_indentation_level() + 4)
        # forward the class statement and the prefix lines to the class context
        for prefix_comment_line in prefix_comment_lines:
            class_facet_context.process_line(prefix_comment_line)
        class_facet_context.process_line(class_facet_statement_line)
        self.push_child_context(class_facet_context)

    def validate_contents(self):
        """
            called by the framework after processing the file, to validate the overall contents of the context
        """
        ContextBaseClass.validate_contents(self)
        if not (self.get_content_class_prefix_comments() or self.get_content_class_suffix_comment()):
            self.error("CLASS-MUST-BE-COMMENTED", "a YAPL class must be commented, either using prefix- or suffix-notation", None)
        if not self.get_content_class_facets():
            self.error("CLASS-MUST-HAVE-FACETS", "a YAPL class must have one or more facets", None)

    def get_content_class_name(self):
        """
            Retrieves the class-name of this ClassContext, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__class_name

    def get_content_class_prefix_comments(self):
        """
            Retrieves the prefix-comments of this class, as they shall be exposed to the abstract-syntax-tree
        """
        return self.__prefix_comments

    def get_content_class_suffix_comment(self):
        """
            Retrieves the suffix-comment of this class, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__suffix_comment

    def get_content_class_facets(self):
        """
            retrieves the list of facets contained within this class, which should be > 0 for a valid YAPL file
        """
        facets = []
        contents = self.get_contents()
        for content in contents:
            if isinstance(content, ClassFacetContext):
                facets.append(content)
        return facets
