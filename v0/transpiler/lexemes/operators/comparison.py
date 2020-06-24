from .operator import OperatorLexeme
from .assignment import AssignmentOperatorLexeme


class ComparisonOperatorLexeme(OperatorLexeme):

    lexeme_id = "operators.comparison"

    def precedence(self):
        return len(self.operator) + AssignmentOperatorLexeme.PRECEDENCE


ComparisonOperatorLexeme.register([
    "<", ">", "<=", ">=", "==", "!="
])
