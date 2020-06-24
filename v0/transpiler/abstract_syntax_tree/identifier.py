import re


class Identifier(object):

    def __init__(self, tokens):
        match = self.__pattern.match(tokens.popleft())
        self.identifier = match.group("identifier")

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"identifiers.identifier\((?P<identifier>[^\)]+)\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None