from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class IntegerLexeme(DynamicSymbolLexeme):

    lexeme_id = "primitives.integer"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


IntegerLexeme.register([
    "int8", "int16", "int32", "int64", "int128", "intN"
])
