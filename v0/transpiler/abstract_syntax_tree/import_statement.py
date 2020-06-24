import re

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .identifier import Identifier
from .list_separator import ListSeparator


class ImportStatementUnexpectedToken(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class FromKeyword(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"keywords\.keyword\(from\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 2:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class ImportKeyword(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"keywords\.keyword\(import\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 2:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class ImportStatement(object):

    def __init__(self, tokens, parent):
        self.parent = parent
        self.ast_state = "MATCHED"
        self.source = None
        self.symbols = None

    @classmethod
    def matches(cls, tokens):
        return ImportKeyword.matches(tokens) or FromKeyword.matches(tokens)

    def gobble(self, tokens):
        if self.ast_state == "MATCHED":
            if ImportKeyword.matches(tokens):
                self.ast_state = "IMPORT_SOURCE"
                ImportKeyword(tokens)
                return self
            elif FromKeyword.matches(tokens):
                self.ast_state = "FROM_SOURCE"
                FromKeyword(tokens)
                return self
        elif self.ast_state == "IMPORT_SOURCE":
            if Identifier.matches(tokens):
                self.source = Identifier(tokens)
                return self.parent
        elif self.ast_state == "FROM_SOURCE":
            if Identifier.matches(tokens):
                self.source = Identifier(tokens)
                self.symbols = []
                self.ast_state = "FROM_SOURCE_IMPORT"
                return self
        elif self.ast_state == "FROM_SOURCE_IMPORT":
            if ImportKeyword.matches(tokens):
                ImportKeyword(tokens)
                self.ast_state = "EXPECTING_IDENTIFIER"
                return self
        elif self.ast_state == "EXPECTING_IDENTIFIER":
            if Identifier.matches(tokens):
                self.symbols.append(Identifier(tokens))
                self.ast_state = "EXPECTING_LIST_SEPARATOR_OR_DONE"
                return self
        elif self.ast_state == "EXPECTING_LIST_SEPARATOR_OR_DONE":
            if ListSeparator.matches(tokens):
                ListSeparator(tokens)
                self.ast_state = "EXPECTING_IDENTIFIER"
                return self
            else:
                return self.parent
        raise ImportStatementUnexpectedToken()
