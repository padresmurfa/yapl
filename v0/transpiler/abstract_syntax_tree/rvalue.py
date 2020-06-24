from .literal import Literal
from .function_call import FunctionCall
from .identifier import Identifier


class Rvalue(object):

    def __init__(self, parent):
        self.parent = parent
        self.value = None

    def gobble(self, tokens):
        if Literal.matches(tokens):
            self.value = Literal(tokens)
            return self.parent
        elif FunctionCall.matches(tokens):
            self.value = FunctionCall(tokens, self.parent)
            return self.value
        elif Identifier.matches(tokens):
            self.value = Identifier(tokens)
            return self.parent
        # TODO: expression
        return self.parent
