from ..base.fixed_symbol import FixedSymbolLexeme
from ..identifier import IdentifierLexeme


class LiteralOptionalNoneLexeme(FixedSymbolLexeme):

    lexeme_id = "literals.optional"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE

    symbol = "None"

    @classmethod
    def try_extract(cls, *args):
        return FixedSymbolLexeme.try_extract(cls, *args)


LiteralOptionalNoneLexeme.register()
