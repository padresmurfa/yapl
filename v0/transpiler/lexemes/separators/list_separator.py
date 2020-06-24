from .separator import SeparatorLexeme


class ListSeparatorLexeme(SeparatorLexeme):

    lexeme_id = "separators.list_separator"
    symbol = ","


ListSeparatorLexeme.register()
