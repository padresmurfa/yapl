from .base.dynamic_symbol import DynamicSymbolLexeme


class DelimiterSymbolLexeme(DynamicSymbolLexeme):

    lexeme_id = "delimiters.delimiter"


DelimiterSymbolLexeme.register([
    ".", ",", ":"
])
