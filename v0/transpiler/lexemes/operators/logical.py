from .operator import OperatorLexeme
from ..identifier import IdentifierLexeme


class LogicalOperatorLexeme(OperatorLexeme):

    lexeme_id = "operators.logical"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


LogicalOperatorLexeme.register([
    "and", "or", "xor", "not", "is"
])
