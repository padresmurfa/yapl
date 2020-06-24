from collections import deque

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .identifier import Identifier
from .assignment_operator import AssignmentOperator
from .list_separator import ListSeparator


class LvalueUnexpectedToken(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class Lvalue(object):

    def __init__(self, tokens, parent):
        self.identifiers = []
        self.parent = parent
        self.ast_state = "EXPECTING_IDENTIFIER"

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 2:
            return False
        if not Identifier.matches(tokens):
            return False
        next_token = 1
        while next_token < len(tokens):
            t = deque([tokens[next_token]])
            if AssignmentOperator.matches(t):
                return True
            if not ListSeparator.matches(t):
                return False
            next_token += 1
            if next_token < len(tokens):
                t = deque([tokens[next_token]])
                if not Identifier.matches(t):
                    return False
                next_token += 1

        return False

    def gobble(self, tokens):
        if self.ast_state == "EXPECTING_IDENTIFIER":
            if Identifier.matches(tokens):
                self.identifiers.append(Identifier(tokens))
                self.ast_state = "EXPECTING_LISTSEPARATOR_OR_ASSIGNMENT"
                return self
        elif self.ast_state == "EXPECTING_LISTSEPARATOR_OR_ASSIGNMENT":
            if ListSeparator.matches(tokens):
                ListSeparator(tokens)
                self.ast_state = "EXPECTING_IDENTIFIER"
                return self
            elif AssignmentOperator.matches(tokens):
                return self.parent
        raise LvalueUnexpectedToken()
