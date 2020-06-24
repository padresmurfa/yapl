import re

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .rvalue import Rvalue


class ReturnValueUnexpectedToken(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class ReturnValue(object):

    def __init__(self, tokens, parent):
        tokens.popleft()
        self.ast_state = "EXPECTING_RVALUE"
        self.return_value = None
        self.parent = parent

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"control_flow.function\(return\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 2:
            return False
        return cls.__pattern.match(tokens[0]) is not None

    def gobble(self, tokens):
        if self.ast_state == "EXPECTING_RVALUE":
            rvalue = Rvalue(self)
            self.return_value = rvalue
            self.ast_state = "RVALUE"
            return rvalue
        elif self.ast_state == "RVALUE":
            return self.parent
        raise ReturnValueUnexpectedToken()
