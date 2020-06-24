from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class FloatingPointLexeme(DynamicSymbolLexeme):

    lexeme_id = "primitives.float"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


FloatingPointLexeme.register([
    "float32", "float64"
])
