from .base.dynamic_symbol import DynamicSymbolLexeme
from .identifier import IdentifierLexeme


class OptionalLexeme(DynamicSymbolLexeme):

    lexeme_id = "optionals.optional"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


OptionalLexeme.register([
    "optional",
    "some"          # requires a generic param, e.g. some(1) = some(int8)
])
