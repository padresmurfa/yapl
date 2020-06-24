import re


class AssignmentOperator(object):

    def __init__(self, tokens):
        operator = self.__pattern.match(tokens.popleft()).group("operator")
        self.operator = operator
        self.is_mutable = (operator == ":=") or (operator == "+=") or (operator == "-=") or (operator == "/=") or (operator == "*=")
        self.is_immutable = not self.is_mutable

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"operators.assignment\((?P<operator>[:\+-/\*]?=)\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class ImmutableAssignmentOperator(AssignmentOperator):

    def __init__(self, tokens):
        AssignmentOperator.__init__(self, tokens)

    __immutable_assignment_pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"operators.assignment\(=\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__immutable_assignment_pattern.match(tokens[0]) is not None
