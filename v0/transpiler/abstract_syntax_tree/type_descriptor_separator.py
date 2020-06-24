import re


class TypeDescriptorSeparator(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"separators.type_descriptor"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None