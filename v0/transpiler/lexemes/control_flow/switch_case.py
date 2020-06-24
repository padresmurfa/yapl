from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class SwitchCaseLexeme(DynamicSymbolLexeme):

    lexeme_id = "control_flow.switch_case"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


SwitchCaseLexeme.register([
    "switch", "case"
])
