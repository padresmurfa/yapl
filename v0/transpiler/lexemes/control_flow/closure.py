from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class ClosureLexeme(DynamicSymbolLexeme):

    lexeme_id = "control_flow.closure"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


# closures also make use of returns and return from functions
ClosureLexeme.register([
    "closure", "over"
])
