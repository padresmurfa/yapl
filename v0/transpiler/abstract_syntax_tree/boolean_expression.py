import re

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .parenthesis import ParenthesisOpen, ParenthesisClose
from .identifier import Identifier
from .function_call import FunctionCall
from .literal import BooleanLiteral, OptionalLiteral


class BooleanExpressionUnexpectedToken(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class And(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"operators.logical\(and\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 2:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class Or(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"operators.logical\(or\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 2:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class Not(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"operators.logical\(not\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 2:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class Xor(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"operators.logical\(xor\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 2:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class Is(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"operators.logical\(is\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 2:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class BooleanSubExpression(object):

    def __init__(self, tokens, parent):
        ParenthesisOpen(tokens)
        self.parent = parent
        self.subexpression = None

    @classmethod
    def matches(cls, tokens):
        return ParenthesisOpen.matches(tokens)

    def gobble(self, tokens):
        if BooleanExpression.matches(tokens):
            self.subexpression = BooleanExpression(tokens, self)
            return self.subexpression
        elif ParenthesisClose.matches(tokens):
            return self.parent
        else:
            raise BooleanExpressionUnexpectedToken()


class BooleanExpression(object):

    def __init__(self, tokens, parent):
        self.parent = parent
        self.operation = []

    @classmethod
    def matches(cls, tokens):
        if And.matches(tokens) or Or.matches(tokens) or Not.matches(tokens) or Xor.matches(tokens) or Is.matches(tokens):
            return True
        if ParenthesisOpen.matches(tokens):
            return True
        if Identifier.matches(tokens):
            return True
        if FunctionCall.matches(tokens):
            return True
        if BooleanLiteral.matches(tokens):
            return True
        return False

    def gobble(self, tokens):
        if And.matches(tokens):
            self.operation.append(And(tokens))
            return self
        elif Or.matches(tokens):
            self.operation.append(Or(tokens))
            return self
        elif Not.matches(tokens):
            self.operation.append(Not(tokens))
            return self
        elif Xor.matches(tokens):
            self.operation.append(Xor(tokens))
            return self
        elif Is.matches(tokens):
            self.operation.append(Is(tokens))
            return self
        elif FunctionCall.matches(tokens):
            function_call = FunctionCall(tokens, self)
            self.operation.append(function_call)
            return function_call
        elif Identifier.matches(tokens):
            identifier = Identifier(tokens)
            self.operation.append(identifier)
            return self
        elif BooleanLiteral.matches(tokens):
            self.operation.append(BooleanLiteral(tokens))
            return self
        elif OptionalLiteral.matches(tokens):
            self.operation.append(OptionalLiteral(tokens))
            return self
        elif BooleanSubExpression.matches(tokens):
            return True
        elif ParenthesisClose.matches(tokens):
            return self.parent

        raise BooleanExpressionUnexpectedToken()
