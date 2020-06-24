from ..base.dynamic_symbol import DynamicSymbolLexeme


class OperatorLexeme(DynamicSymbolLexeme):

    def __init__(self, context, lexeme):
        DynamicSymbolLexeme.__init__(self, context, lexeme)
        self.operator = lexeme

    def __repr__(self):
        return DynamicSymbolLexeme.__repr__(self)[:-1] + ", operator=" + self.operator + ")"

    def to_intermediate_repr(self):
        return "{}({})".format(self.lexeme_id, self.operator)
