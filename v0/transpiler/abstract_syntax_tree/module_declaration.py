import re

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .class_declaration import ClassDeclaration
from .curlies import CurlyOpen, CurlyClose
from .identifier import Identifier
from .function_declaration import FunctionDeclaration
from .assignment import Assignment
from .comment import Comment
from .import_statement import ImportStatement


class ModuleMissingIdentifier(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class ModuleUnexpectedToken(TranspilerSyntaxError):
    def __init__(self, offending_token):
        TranspilerSyntaxError.__init__(self, offending_token)


class ModuleMissingOpeningCurly(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class ModuleMissingClosingCurly(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class ModuleDeclaration(object):

    def __init__(self, tokens, parent):
        tokens.popleft()
        self.parent = parent
        self.ast_state = "UNIDENTIFIED"
        self.identifier = None
        self.contents = []

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"keywords.keyword\(module\)"
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
                raise ModuleMissingIdentifier()
            if Identifier.matches(tokens):
                self.identifier = Identifier(tokens)
                self.ast_state = "IDENTIFIED"
                return self
        elif self.ast_state == "IDENTIFIED":
            if len(tokens) == 0:
                raise ModuleMissingOpeningCurly()
            if CurlyOpen.matches(tokens):
                CurlyOpen(tokens)
                self.ast_state = "CONTENTS"
                return self
        elif self.ast_state == "CONTENTS":
            if len(tokens) == 0:
                raise ModuleMissingClosingCurly()
            elif CurlyClose.matches(tokens):
                CurlyClose(tokens)
                return self.parent
            elif Assignment.matches(tokens):
                assignment = Assignment(tokens, self)
                self.contents.append(assignment)
                return assignment
            elif ClassDeclaration.matches(tokens):
                class_declaration = ClassDeclaration(tokens, self)
                self.contents.append(class_declaration)
                return class_declaration
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
        raise ModuleUnexpectedToken(tokens[0])
