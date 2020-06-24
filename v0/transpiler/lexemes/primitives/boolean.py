from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class BooleanLexeme(DynamicSymbolLexeme):

    lexeme_id = "primitives.boolean"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


BooleanLexeme.register([
    "bool", "boolean"
])
