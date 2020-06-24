import re
import base64


class BooleanLiteral(object):

    def __init__(self, tokens):
        self.value = self.__pattern_true.match(tokens.popleft()) is not None

    __pattern_true = re.compile(
        r"\[\d+.\d+\]:"
        r"literals.boolean\(true\)"
    )

    __pattern_false = re.compile(
        r"\[\d+.\d+\]:"
        r"literals.boolean\(false\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        if cls.__pattern_true.match(tokens[0]) is not None:
            return True
        if cls.__pattern_false.match(tokens[0]) is not None:
            return True
        return False


class OptionalLiteral(object):

    def __init__(self, tokens):
        self.value = self.__pattern.match(tokens.popleft()) is not None

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"literals.optional\(None\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None


# TODO: have separate literal classes for each type, use Literal as a container
class Literal(object):

    def __init__(self, tokens):
        match = self.__pattern.match(tokens.popleft())
        self.type = match.group("type")
        value = match.group("value")
        if self.type == "string":
            self.value = base64.b64decode(value)
        else:
            self.value = value

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"literals.(?P<type>[^\(]+)\((?P<value>[^\)]+)\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None


