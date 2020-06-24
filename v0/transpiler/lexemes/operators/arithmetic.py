from .operator import OperatorLexeme
from .assignment import AssignmentOperatorLexeme


class ArithmeticOperatorLexeme(OperatorLexeme):

    PRECEDENCE = 1 + AssignmentOperatorLexeme.PRECEDENCE

    lexeme_id = "operators.arithmetic"


ArithmeticOperatorLexeme.register([
    "+", "-", "*", "/"
])
