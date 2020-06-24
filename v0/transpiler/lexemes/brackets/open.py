from ..base.fixed_symbol import FixedSymbolLexeme


class BracketsOpenLexeme(FixedSymbolLexeme):

    symbol = "["
    lexeme_id = "bracket.open"

    def to_intermediate_repr(self):
        return "{}".format(self.lexeme_id)

    @classmethod
    def try_extract(cls, *args):
        return FixedSymbolLexeme.try_extract(cls, *args)


BracketsOpenLexeme.register()
