from transpiler.frontend.contexts.context import ContextBaseClass

class IdentifierDeclarationContext(ContextBaseClass):
    """
        A context-sensitive parser for parsing a identifier-declaration within a YAPL-class
    """

    def __init__(self, parent_class_context, indentation_level):
        """
            initializes the IdentifierDeclarationContext

            'parent_class_context' is the ClassContext that contains this IdentifierDeclarationContext
        """
        ContextBaseClass.__init__(self, None, parent_class_context, "IDENTIFIERDECLARATION", indentation_level)
        self.__identifier_name = None
        self.__identifier_value_or_reference = None
        self.__identifier_type = None
        self.__prefix_comments = []
        self.__suffix_comment = ""

    def get_name(self):
        """
            retrieves the name of this context
        """
        return self.__identifier_name if self.__identifier_name is not None else "<unknown>"

    def __str__(self):
        return "YAPL frontend identifier-declaration context for identifier-declaration '{}'".format(self.get_fully_qualified_name())

    def process_line(self, lexer_line):
        """
            called by the framework to process a line
        """
        ContextBaseClass.push_lexer_line(self, lexer_line)
        leading_token = lexer_line.peek_leading_token()
        if leading_token.get_offset() == self.get_indentation_level():
            self.__process_line_identifier_statement(leading_token)
        elif leading_token.is_empty_line():
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-CONTENT-AT-INDENT", "identifier-declaration declarations may only include direct content at indent level N", leading_token)

    def __process_line_identifier_statement(self, leading_token):
        """
            Helper function for process_line that handles the leading identifier declaration statement
        """
        if leading_token.is_identifier():
            self.__process_line_identifier_declaration_statement(leading_token)
        elif leading_token.is_comment():
            self.trace("prefix comment statement encountered", leading_token)
            self.__prefix_comments.append(leading_token.get_lexeme_value())
            ContextBaseClass.pop_lexer_line(self)
        elif leading_token.is_empty_line():
            self.trace("empty line statement encountered", leading_token)
            ContextBaseClass.pop_lexer_line(self)
        else:
            self.error("EXPECTED-IDENTIFIER-DECLARATION-STATEMENT", "identifier declarations may only include the actual identifier-declaration-statement", leading_token)

    def __process_line_identifier_declaration_statement(self, identifier_name_token):
        """
            Helper function for process_line that handles the leading identifier declaration statement
        """
        self.trace("identifier-declaration-statement encountered", identifier_name_token)
        self.__identifier_name = identifier_name_token.get_lexeme_value()
        lexer_line = self.peek_lexer_line().consume(identifier_name_token)
        identifier_value_or_reference_token = lexer_line.peek_leading_token()
        if not identifier_value_or_reference_token.is_identifier_declaration_type():
            self.error("EXPECTED-IDENTIFIER-DECLARATION-TYPE-IDENTIFIER-DECLARATION-STATEMENT", "identifier-declaration statements must specify an is/references relationship between the identifier and the type", identifier_value_or_reference_token)
        else:
            self.__identifier_value_or_reference = identifier_value_or_reference_token.get_lexeme_value()
            lexer_line = lexer_line.consume(identifier_value_or_reference_token)
            identifier_type_token = lexer_line.peek_leading_token()
            if not identifier_type_token.is_unqualified_identifier():
                self.error("EXPECTED-IDENTIFIER-TYPE-DECLARATION", "identifier-declaration statements must specify a type for the identifier", identifier_value_or_reference_token)
            else:
                self.__identifier_type = identifier_type_token.get_lexeme_value()
                lexer_line = lexer_line.consume(identifier_type_token)
                # now there might be an optional suffix comment
                suffix_comment = lexer_line.peek_leading_token()
                if suffix_comment.is_end_of_line():
                    pass
                elif suffix_comment.is_comment_horizontal_rule():
                    self.error("EXPECTED-SUFFIX-COMMENT-FOR-IDENTIFIER-DECLARATION-NOT-HORIZONTAL-RULE", "identifier declaration statements may have suffix comments, but a horizontal rule may not be used as a suffix comment", suffix_comment)
                elif suffix_comment.is_comment():
                    self.__suffix_comment = suffix_comment.get_lexeme_value()
                else:
                    self.error("EXPECTED-SUFFIX-COMMENT-FOR-IDENTIFIER-DECLARATION", "identifier declaration statements may only be followed by suffix comments in the same line", suffix_comment)
        ContextBaseClass.pop_lexer_line(self)

    def validate_contents(self):
        """
            called by the framework after processing the file, to validate the overall contents of the context
        """
        ContextBaseClass.validate_contents(self)
        if not self.get_content_identifier_name():
            self.error("IDENTIFIER-DECLARATION-MUST-HAVE-NAME", "a YAPL identifier-declaration must have a name", None)
        if not self.get_content_identifier_value_or_reference():
            self.error("IDENTIFIER-DECLARATION-MUST-BE-VALUE-OR-REFERENCE", "a YAPL identifier-declaration must be declared to be a value or a reference", None)
        if not self.get_content_identifier_type():
            self.error("IDENTIFIER-DECLARATION-MUST-HAVE-TYPE", "a YAPL identifier-declaration must have a type", None)
        if not (self.get_content_identifier_prefix_comments() or self.get_content_identifier_suffix_comment()):
            self.error("IDENTIFIER-MUST-BE-COMMENTED", "a YAPL identifier must be commented, either using prefix- or suffix-notation", None)

    def get_content_identifier_name(self):
        """
            Retrieves the name of this identifier-declaration, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__identifier_name

    def get_content_identifier_value_or_reference(self):
        """
            Retrieves whether this identifier-declaration is a value or a reference, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__identifier_value_or_reference

    def get_content_identifier_type(self):
        """
            Retrieves the type of this identifier-declaration, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__identifier_type

    def get_content_identifier_prefix_comments(self):
        """
            Retrieves the prefix-comments of this identifier, as they shall be exposed to the abstract-syntax-tree
        """
        return self.__prefix_comments

    def get_content_identifier_suffix_comment(self):
        """
            Retrieves the suffix-comment of this identifier, as it shall be exposed to the abstract-syntax-tree
        """
        return self.__suffix_comment
