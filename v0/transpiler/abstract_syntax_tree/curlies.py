import re


class CurlyOpen(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"curlies.open"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class CurlyClose(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"curlies.close"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None
