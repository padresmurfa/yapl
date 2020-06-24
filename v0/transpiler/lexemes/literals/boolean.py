from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class LiteralBooleanLexeme(DynamicSymbolLexeme):

    lexeme_id = "literals.boolean"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


LiteralBooleanLexeme.register([
    "true", "false"
])
