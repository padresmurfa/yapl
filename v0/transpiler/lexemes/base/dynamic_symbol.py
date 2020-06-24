from .lexeme import Lexeme
from .registry.lexeme_registry import LexemeRegistry
from ...lexer.context import Context


class DynamicSymbolLexeme(Lexeme):

    def __init__(self, context, lexeme):
        Lexeme.__init__(self, context, lexeme)
        self.lexeme = lexeme

    def __repr__(self):
        return Lexeme.__repr__(self)[:-1] + ", symbol=" + self.lexeme + ")"

    def to_intermediate_repr(self):
        return "{}({})".format(self.lexeme_id, self.lexeme)

    class Factory(object):

        def __init__(self, cls, symbol):
            self.__cls = cls
            self.__symbol = symbol

        def try_extract(self, source, context):
            if source.startswith(self.__symbol):
                lexeme = self.__cls(context, self.__symbol)
                remainder = lexeme.remainder(source)
                if not Lexeme.splits_identifier(self.__symbol, remainder):
                    return lexeme, remainder, lexeme.next_context()
            return None, source, context

        def precedence(self):
            return self.__cls(Context.EMPTY, self.__symbol).precedence()

    @classmethod
    def register(cls, symbols):
        for symbol in symbols:
            LexemeRegistry.register(DynamicSymbolLexeme.Factory(cls, symbol))
