import base64
import re

from ..base.lexeme import Lexeme


class LiteralStringLexeme(Lexeme):

    lexeme_id = "literals.string"

    def __init__(self, context, lexeme, value):
        Lexeme.__init__(self, context, lexeme)
        self.__value = value

    def __repr__(self):
        return Lexeme.__repr__(self)[:-1] + ", value=\"" + self.__value + "\")"

    def to_intermediate_repr(self):
        value_as_bytes = base64.b64encode(self.__value.encode("utf-8"))
        value_as_string = str(value_as_bytes, "utf-8")
        return "{}({})".format(self.lexeme_id, value_as_string)

    @staticmethod
    def try_extract(source, context):
        if source.startswith("\""):
            lexeme = LiteralStringLexeme.get_quoted_string(source, context)
            return lexeme, lexeme.remainder(source), lexeme.next_context()
        return None, source, context

    class PreConditionViolationError(Exception):
        pass

    @staticmethod
    def get_quoted_string(text, context):
        regex_quoted_string = r"^\"([^\"\\]*(?:\\.[^\"\\]*)*)\""
        x = re.search(regex_quoted_string, text)
        if x is None:
            raise LiteralStringLexeme.PreConditionViolationError("Contract violation: get_quoted_string should never be called for strings that do not immediately start with a quote")
        return LiteralStringLexeme(context, x.group(0), x.group(0)[1:-1])


LiteralStringLexeme.register()
