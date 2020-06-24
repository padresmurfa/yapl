from ..base.fixed_symbol import FixedSymbolLexeme


class CurlyBracketOpenLexeme(FixedSymbolLexeme):

    symbol = "{"
    lexeme_id = "curlies.open"

    def to_intermediate_repr(self):
        return "{}".format(self.lexeme_id)

    @classmethod
    def try_extract(cls, *args):
        return FixedSymbolLexeme.try_extract(cls, *args)


CurlyBracketOpenLexeme.register()
