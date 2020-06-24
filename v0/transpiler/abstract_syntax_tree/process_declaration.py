import re

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .curlies import CurlyOpen, CurlyClose
from .identifier import Identifier
from .function_declaration import FunctionDeclaration
from .comment import Comment
from .import_statement import ImportStatement

class ProcessMissingIdentifier(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class ProcessUnexpectedToken(TranspilerSyntaxError):
    def __init__(self, offending_token):
        TranspilerSyntaxError.__init__(self, offending_token)


class ProcessMissingOpeningCurly(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class ProcessMissingClosingCurly(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class ProcessDeclaration(object):

    def __init__(self, tokens, parent):
        tokens.popleft()
        self.parent = parent
        self.ast_state = "UNIDENTIFIED"
        self.identifier = None
        self.contents = []

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"keywords.keyword\(process\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None

    def gobble(self, tokens):
        # TODO: some types of comments are allowed in some of these states
        if self.ast_state == "UNIDENTIFIED":
            if len(tokens) == 0:
                raise ProcessMissingIdentifier()
            if Identifier.matches(tokens):
                self.identifier = Identifier(tokens)
                self.ast_state = "IDENTIFIED"
                return self
        elif self.ast_state == "IDENTIFIED":
            if len(tokens) == 0:
                raise ProcessMissingOpeningCurly()
            if CurlyOpen.matches(tokens):
                CurlyOpen(tokens)
                self.ast_state = "CONTENTS"
                return self
        elif self.ast_state == "CONTENTS":
            if len(tokens) == 0:
                raise ProcessMissingClosingCurly()
            elif CurlyClose.matches(tokens):
                CurlyClose(tokens)
                return self.parent
            elif FunctionDeclaration.matches(tokens):
                function_declaration = FunctionDeclaration(tokens, self)
                self.contents.append(function_declaration)
                return function_declaration
            elif ImportStatement.matches(tokens):
                import_statement = ImportStatement(tokens, self)
                self.contents.append(import_statement)
                return import_statement
            elif Comment.matches(tokens):
                comment = Comment(self)
                self.contents.append(comment)
                return comment
        raise ProcessUnexpectedToken(tokens[0])
