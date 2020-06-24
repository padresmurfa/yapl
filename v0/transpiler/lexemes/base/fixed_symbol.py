from .lexeme import Lexeme


class FixedSymbolLexeme(Lexeme):

    # declare symbol in the subclass
    # symbol = None

    def __repr__(self):
        return Lexeme.__repr__(self)[:-1] + ", symbol=" + self.__class__.symbol + ")"

    def to_intermediate_repr(self):
        return "{}({})".format(self.lexeme_id, self.__class__.symbol)

    @staticmethod
    def try_extract(cls, source, context):
        if source.startswith(cls.symbol):
            lexeme = cls(context, cls.symbol)
            remainder = lexeme.remainder(source)
            if not Lexeme.splits_identifier(cls.symbol, remainder):
                return lexeme, remainder, lexeme.next_context()
        return None, source, context
