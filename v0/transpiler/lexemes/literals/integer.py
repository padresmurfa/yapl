import re

from ..base.lexeme import Lexeme


class LiteralIntegerLexeme(Lexeme):

    PRECEDENCE = 0

    lexeme_id = "literals.integer"

    def __init__(self, context, lexeme, value):
        Lexeme.__init__(self, context, lexeme)
        self.__value = value

    def __repr__(self):
        return Lexeme.__repr__(self)[:-1] + ", value=\"" + self.__value + "\")"

    def to_intermediate_repr(self):
        return "{}({})".format(self.lexeme_id, self.__value)

    @staticmethod
    def try_extract(source, context):
        regex_number = r"^[+\-]?[0-9]+"
        x = re.search(regex_number, source)
        if x is None:
            return None, source, context
        lexeme = LiteralIntegerLexeme(context, x.group(0), x.group(0))
        return lexeme, lexeme.remainder(source), lexeme.next_context()


LiteralIntegerLexeme.register()
