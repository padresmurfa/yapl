from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class FunctionLexeme(DynamicSymbolLexeme):

    lexeme_id = "control_flow.function"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


FunctionLexeme.register([
    "function", "coroutine", "return", "returns"
])
