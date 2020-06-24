from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class BinaryLexeme(DynamicSymbolLexeme):

    lexeme_id = "primitives.binary"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


BinaryLexeme.register([
    "bit", "bits", "byte", "bytes"
])
