from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class UnsignedIntegerLexeme(DynamicSymbolLexeme):

    lexeme_id = "primitives.unsigned"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


UnsignedIntegerLexeme.register([
    "uint8", "uint16", "uint32", "uint64", "uint128", "uintN"
])
