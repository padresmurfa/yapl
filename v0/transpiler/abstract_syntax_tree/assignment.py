from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .lvalue import Lvalue
from .assignment_operator import AssignmentOperator
from .rvalue import Rvalue


class AssignmentUnexpectedToken(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class Assignment(object):

    def __init__(self, tokens, parent):
        self.parent = parent
        self.lvalue = None
        self.operator = None
        self.rvalue = None
        self.ast_state = "BEFORE_LVALUE"

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 3:
            return False
        if not Lvalue.matches(tokens):
            return False
        return True

    def gobble(self, tokens):
        if self.ast_state == "BEFORE_LVALUE":
            lvalue = Lvalue(tokens, self)
            self.lvalue = lvalue
            self.ast_state = "ASSIGNMENT"
            return lvalue
        elif self.ast_state == "ASSIGNMENT":
            if AssignmentOperator.matches(tokens):
                self.operator = AssignmentOperator(tokens)
                self.ast_state = "BEFORE_RVALUE"
                return self
        elif self.ast_state == "BEFORE_RVALUE":
            rvalue = Rvalue(self.parent)
            self.ast_state = "RVALUE"
            self.rvalue = rvalue
            return rvalue
        elif self.ast_state == "RVALUE":
            return self.parent
        raise AssignmentUnexpectedToken()
