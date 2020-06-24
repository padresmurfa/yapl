from ..base.fixed_symbol import FixedSymbolLexeme


class ParenthesisOpenLexeme(FixedSymbolLexeme):

    symbol = "("
    lexeme_id = "parenthesis.open"

    def to_intermediate_repr(self):
        return "{}".format(self.lexeme_id)

    @classmethod
    def try_extract(cls, *args):
        return FixedSymbolLexeme.try_extract(cls, *args)


ParenthesisOpenLexeme.register()
