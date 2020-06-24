from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class TryCatchFinallyLexeme(DynamicSymbolLexeme):

    lexeme_id = "control_flow.try_catch_finally"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


TryCatchFinallyLexeme.register([
    "try", "catch", "finally", "throw"
])
