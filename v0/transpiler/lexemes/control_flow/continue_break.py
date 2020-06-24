from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class ContinueBreakLexeme(DynamicSymbolLexeme):

    lexeme_id = "control_flow.continue_break"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


ContinueBreakLexeme.register([
    "continue", "break", "redo", "retry"
])
