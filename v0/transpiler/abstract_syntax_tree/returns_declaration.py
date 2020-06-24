import re


class ReturnsDeclaration(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"control_flow.function\(returns\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None
