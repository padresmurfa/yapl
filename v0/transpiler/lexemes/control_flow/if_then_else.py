from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class IfThenElseSymbolLexeme(DynamicSymbolLexeme):

    lexeme_id = "control_flow.if_then_else"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


IfThenElseSymbolLexeme.register([
    "if", "else"
])
