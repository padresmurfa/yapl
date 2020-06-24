from .separator import SeparatorLexeme


class DotSeparatorLexeme(SeparatorLexeme):

    lexeme_id = "separators.dot_separator"
    symbol = "."


DotSeparatorLexeme.register()
