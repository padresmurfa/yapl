from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class ForLoopLexeme(DynamicSymbolLexeme):

    lexeme_id = "control_flow.for_loop"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


ForLoopLexeme.register([
    "for", "in"
])
