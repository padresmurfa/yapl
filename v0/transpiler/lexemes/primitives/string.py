from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class StringLexeme(DynamicSymbolLexeme):

    lexeme_id = "primitives.string"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


StringLexeme.register([
    "char", "string",
    "char8", "string8"
])
