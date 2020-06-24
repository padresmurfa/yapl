from .separator import SeparatorLexeme


class TypeDescriptorLexeme(SeparatorLexeme):

    lexeme_id = "separators.type_descriptor"
    symbol = ":"


TypeDescriptorLexeme.register()
