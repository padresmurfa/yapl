from .operator import OperatorLexeme


class AssignmentOperatorLexeme(OperatorLexeme):

    PRECEDENCE = 0
    lexeme_id = "operators.assignment"


AssignmentOperatorLexeme.register([
    "=", ":=", "+=", "-=", "/=", "*="
])
