from .operator import OperatorLexeme


class ReferenceOperatorLexeme(OperatorLexeme):

    lexeme_id = "operators.reference"


ReferenceOperatorLexeme.register([
    "&"
])
