from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class DoWhileLoopLexeme(DynamicSymbolLexeme):

    lexeme_id = "control_flow.do_while_loop"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


DoWhileLoopLexeme.register([
    "do", "while", "until"
])
