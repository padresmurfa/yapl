from ..base.fixed_symbol import FixedSymbolLexeme


class SeparatorLexeme(FixedSymbolLexeme):

    def __init__(self, context, lexeme):
        FixedSymbolLexeme.__init__(self, context, lexeme)

    def to_intermediate_repr(self):
        return "{}".format(self.lexeme_id)

    @classmethod
    def try_extract(cls, *args):
        return FixedSymbolLexeme.try_extract(cls, *args)
