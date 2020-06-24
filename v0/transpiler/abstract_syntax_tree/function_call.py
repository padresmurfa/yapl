from collections import deque

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .parenthesis import ParenthesisClose, ParenthesisOpen
from .identifier import Identifier
from .list_separator import ListSeparator
from .dot_separator import DotSeparator


class FunctionCallExpectingAnotherArgument(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class FunctionCallUnexpectedToken(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class FunctionCall(object):

    def __init__(self, tokens, parent):
        self.identifier = Identifier(tokens)
        tokens.popleft()
        self.parent = parent
        self.named_values = []
        self.positional_values = []
        self.chain_to = None
        self.ast_state = "MIGHT_HAVE_AN_ARGUMENT"

    @staticmethod
    def matches(tokens):
        if len(tokens) < 2:
            return False
        if not Identifier.matches(tokens):
            return False
        next_token = deque(list([tokens[1]]))
        if not ParenthesisOpen.matches(next_token):
            return False
        return True

    def gobble(self, tokens):
        if self.ast_state == "MIGHT_HAVE_AN_ARGUMENT" or self.ast_state == "EXPECTING_AN_ARGUMENT":
            from .assignment import Assignment
            if Assignment.matches(tokens):
                named_value = Assignment(tokens, self)
                self.named_values.append(named_value)
                self.ast_state = "MIGHT_HAVE_ANOTHER_ARGUMENT"
                return named_value
            elif ParenthesisClose.matches(tokens):
                if self.ast_state == "EXPECTING_AN_ARGUMENT":
                    raise FunctionCallExpectingAnotherArgument()
            else:
                # if has named value, fuck off
                from .rvalue import Rvalue
                self.ast_state = "MIGHT_HAVE_ANOTHER_ARGUMENT"
                positional_value = Rvalue(self)
                self.positional_values.append(positional_value)
                return positional_value
        else:
            if ListSeparator.matches(tokens):
                ListSeparator(tokens)
                self.ast_state = "EXPECTING_AN_ARGUMENT"
                return self
        if ParenthesisClose.matches(tokens):
            ParenthesisClose(tokens)
            if DotSeparator.matches(tokens):
                DotSeparator(tokens)
                chain_to = FunctionCall(tokens, self.parent)
                self.chain_to = chain_to
                return chain_to
            else:
                return self.parent
        else:
            raise FunctionCallUnexpectedToken()
