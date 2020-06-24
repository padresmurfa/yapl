import re

from .base.lexeme import Lexeme


class IdentifierLexeme(Lexeme):

    PRECEDENCE = 0
    lexeme_id = "identifiers.identifier"

    def __init__(self, context, lexeme, identifier):
        Lexeme.__init__(self, context, lexeme)
        self.identifier = identifier

    def __repr__(self):
        return Lexeme.__repr__(self)[:-1] + ", identifier=\"" + self.identifier + "\")"

    def to_intermediate_repr(self):
        return "{}({})".format(self.lexeme_id, self.identifier)

    @staticmethod
    def try_extract(source, context):
        regex_identifier = r"^[a-zA-Z_][a-zA-Z0-9_\[\]]*(\.[a-zA-Z_][a-zA-Z0-9_\[\]]*)*"
        x = re.search(regex_identifier, source)
        if x is None:
            return None, source, context
        lexeme = IdentifierLexeme(context, x.group(0), x.group(0))
        return lexeme, lexeme.remainder(source), lexeme.next_context()


IdentifierLexeme.register()
