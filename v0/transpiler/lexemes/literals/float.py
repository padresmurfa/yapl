import re

from ..base.lexeme import Lexeme
from .integer import LiteralIntegerLexeme


class LiteralFloatLexeme(Lexeme):

    lexeme_id = "literals.float"

    def __init__(self, context, lexeme, value):
        Lexeme.__init__(self, context, lexeme)
        self.__value = value

    def __repr__(self):
        return Lexeme.__repr__(self)[:-1] + ", value=\"" + self.__value + "\")"

    def to_intermediate_repr(self):
        return "{}({})".format(self.lexeme_id, self.__value)

    @classmethod
    def precedence(cls):
        return 1 + LiteralIntegerLexeme.PRECEDENCE

    @staticmethod
    def try_extract(source, context):
        regex_number = r"^[+\-]?[0-9]+\.[0-9]+([eE][\-\+]\d+)?"
        x = re.search(regex_number, source)
        if x is None:
            return None, source, context
        lexeme = LiteralFloatLexeme(context, x.group(0), x.group(0))
        return lexeme, lexeme.remainder(source), lexeme.next_context()


LiteralFloatLexeme.register()
