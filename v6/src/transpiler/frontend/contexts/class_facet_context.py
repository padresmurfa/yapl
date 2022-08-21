from transpiler.frontend.contexts.context import ContextBaseClass
from transpiler.frontend.contexts.callable_context import CallableContext

class ClassFacetContext(ContextBaseClass):
    """
        A context-sensitive parser for parsing a class-facet within a YAPL-class
    """

    def __init__(self, parent_class_context, indentation_level):
        """
            initializes the ClassFacetContext

            'parent_class_context' is the ClassContext that contains this ClassFacetContext
        """
        ContextBaseClass.__init__(self, None, parent_class_context, "CLASSFACET", indentation_level)
        self.__class_facet_visibility = None
        self.__class_facet_type = None
        self.__class_facet_name = None
        self.__prefix_comments = []
        self.__suffix_comment = ""

    def get_name(self):
        """
            retrieves the name of this context
        """
        return self.__class_facet_name if self.__class_facet_name is not None else "<unknown>"

    def __str__(self):
        return "YAPL frontend class-facet context for class-facet '{}'".format(self.get_fully_qualified_name())

    def process_line(self, lexer_line):
        """
            called by the framework to process a line
        """
        ContextBaseClass.push_lexer_line(self, lexer_line)
        leading_token = lexer_line.peek_leading_token()
        if leading_token.get_offset() == self.get_indentation_level():
            self.__process_line_class_facet_statement_header(leading_token)
        elif leading_token.get_offset() == self.get_indentation_level() + 4:
            self.__process_line_class_facet_body(leading_token)
        elif leading_token.is_empty_line():
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-CONTENT-AT-INDENT-THREE", "class-facet declarations may only include direct content at indent level three (offset: 12 characters)", leading_token)

    def __process_line_class_facet_statement_header(self, leading_token):
        """
            Helper function for process_line that handles the leading class declaration statement
        """
        if leading_token.is_visibility_level():
            self.__process_line_class_facet_statement(leading_token)
        elif leading_token.is_comment():
            self.trace("prefix comment statement encountered", leading_token)
            self.__prefix_comments.append(leading_token.get_lexeme_value())
            ContextBaseClass.pop_lexer_line(self)
        elif leading_token.is_empty_line():
            self.trace("empty line statement encountered", leading_token)
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-PREFIX-COMMENT-OR-CLASS-STATEMENT-AT-INDENT-ONE", "class declarations may only include prefix-comments and the actual class-statement at indent one", leading_token)

    def __process_line_class_facet_statement(self, visibility_token):
        """
            Helper function for process_line that handles the leading class declaration statement
        """
        self.trace("class-facet visibility-declaration encountered", visibility_token)
        self.__class_facet_visibility = visibility_token.get_lexeme_value()
        lexer_line = self.peek_lexer_line().consume(visibility_token)
        class_facet_type_keyword = lexer_line.peek_leading_token()
        if not class_facet_type_keyword.is_class_facet_type():
            self.error("EXPECTED-FACET-KEYWORD", "class-facets require the facet keyword", class_facet_type_keyword)
        else:
            self.__class_facet_type = class_facet_type_keyword.get_lexeme_value()
            lexer_line = lexer_line.consume(class_facet_type_keyword)
            facet_name = lexer_line.peek_leading_token()
            if not facet_name.is_token():
                self.error("EXPECTED-TOKEN", "class-facets must have a name", facet_name)
            elif not facet_name.is_valid_token():
                self.error("EXPECTED-VALID-TOKEN", "class-facet names must be valid tokens", facet_name)
            else:
                self.__class_facet_name = facet_name.get_lexeme_value()
                self.trace("class facet name: {}".format(self.__class_facet_name), facet_name)
                lexer_line = lexer_line.consume(facet_name)
                colon_token = lexer_line.peek_leading_token()
                if not colon_token.is_symbol(":"):
                    self.error("EXPECTED-COLON-TERMINATOR-FOR-CLASS-FACET-STATEMENT", "class-facet statements must be terminated by a colon", colon_token)
                else:
                    lexer_line = lexer_line.consume(colon_token)
                    # now there might be an optional suffix comment
                    suffix_comment = lexer_line.peek_leading_token()
                    if suffix_comment.is_end_of_line():
                        pass
                    elif suffix_comment.is_comment_horizontal_rule():
                        self.error("EXPECTED-SUFFIX-COMMENT-FOR-CLASS-FACET-STATEMENT-NOT-HORIZONTAL-RULE", "class-facet statements may have suffix comments, but a horizontal rule may not be used as a suffix comment", suffix_comment)
                    elif suffix_comment.is_comment():
                        self.__suffix_comment = suffix_comment.get_lexeme_value()
                    else:
                        self.error("EXPECTED-SUFFIX-COMMENT-FOR-CLASS-FACET-STATEMENT", "class-facet statements may only be followed by suffix comments in the same line", suffix_comment)
        ContextBaseClass.pop_lexer_line(self)

    def __process_line_class_facet_body(self, leading_token):
        """
            Helper function for process_line that handles the leading class declaration statement
        """
        if leading_token.is_callable():
            if leading_token.is_callable("constructor") or leading_token.is_callable("method") or leading_token.is_callable("generator"):
                self.__process_line_class_facet_callable_statement()
            else:
                self.error("EXPECTED-METHOD-OR-GENERATOR-METHOD", "class-facets may contain constructors, methods, or generator methods, but cannot contain functions")
        else:
            self.trace("ignoring class-facet content", leading_token)
            # TODO: member variables

    def __process_line_class_facet_callable_statement(self):
        """
            helper function for process_line, which handles lines that contain a callable statement

            Removes the callable statement line and the prefix comment lines from the unprocessed contents, and
            forwards them to a CallableContext object that is created as a child of this object.
        """
        # remove the callable statement and any optional prefix comment lines
        callable_statement_line = self.pop_lexer_line()
        prefix_comment_lines = self.maybe_pop_prefix_comments_at_offset(self.get_indentation_level() + 4)
        # create the callable context, attach it as a child of this context, and pass control to it
        callable_context = CallableContext(self, self.get_indentation_level() + 4)
        # forward the class statement and the prefix lines to the callable
        for prefix_comment_line in prefix_comment_lines:
            callable_context.process_line(prefix_comment_line)
        callable_context.process_line(callable_statement_line)
        self.push_child_context(callable_context)

    def validate_contents(self):
        """
            called by the framework after processing the file, to validate the overall contents of the context
        """
        ContextBaseClass.validate_contents(self)
        if not self.get_content_class_facet_visibility():
            self.error("CLASS-FACET-MUST-HAVE-VISIBILITY", "a YAPL class-facet must have a visibility level", None)
        if not self.get_content_class_facet_type():
            self.error("CLASS-FACET-MUST-HAVE-TYPE", "a YAPL class-facet must have a type (facet, trait, or interface)", None)
        if not self.get_content_class_facet_name():
            self.error("CLASS-FACET-MUST-HAVE-NAME", "a YAPL class-facet must have a name", None)
        if not (self.get_content_callables() or self.get_content_member_variables()):
            self.error("CLASS-FACET-MUST-HAVE-CONTENT", "a YAPL class-facet must have content, either in the form of callables or members", None)

    def get_content_class_facet_visibility(self):
        """
            Retrieves the visibility of this class-facet, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__class_facet_visibility

    def get_content_class_facet_type(self):
        """
            Retrieves the type of this class-facet, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__class_facet_type

    def get_content_class_facet_name(self):
        """
            Retrieves the name of this class-facet, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__class_facet_name

    def get_content_class_prefix_comments(self):
        """
            Retrieves the prefix-comments of this class-facet, as they shall be exposed to the abstract-syntax-tree
        """
        return self.__prefix_comments

    def get_content_class_suffix_comment(self):
        """
            Retrieves the suffix-comment of this class-facet, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__suffix_comment

    def get_content_callables(self):
        """
            retrieves the list of callables contained within this ClassFacetContext
        """
        callables = []
        contents = self.get_contents()
        for content in contents:
            if isinstance(content, CallableContext):
                callables.append(content)
        return callables

    def get_content_member_variables(self):
        """
            retrieves the list of member variables contained within this ClassFacetContext
        """
        member_variables = []
        contents = self.get_contents()
        for content in contents:
            #if isinstance(content, VariableDeclarationContext):
            #    member_variables.append(content)
            # TODO:
            pass
        return member_variables
