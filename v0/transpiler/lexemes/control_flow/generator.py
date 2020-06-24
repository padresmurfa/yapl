from ..base.dynamic_symbol import DynamicSymbolLexeme
from ..identifier import IdentifierLexeme


class GeneratorYieldLexeme(DynamicSymbolLexeme):

    lexeme_id = "control_flow.generator_yield"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


GeneratorYieldLexeme.register([
    "generator", "yield"
])
