from .base.dynamic_symbol import DynamicSymbolLexeme
from .identifier import IdentifierLexeme


class ReservedWordLexeme(DynamicSymbolLexeme):

    lexeme_id = "reserved_words.word"

    @classmethod
    def precedence(cls):
        return 1 + IdentifierLexeme.PRECEDENCE


ReservedWordLexeme.register([
    "repeat",               # repeat is not necessary in the family: do-while, do-until, while() {}, until() {}
    "goto", "label",        # goto's are considered harmful. accept it.
    "null", "undefined",    # use None instead of null. Undefined is not a construct in many/most languages.
    "default",              # switch-case statements require all cases to be explicit
    "method",               # a method is a function that has an implicit this pointer
    "classmethod",          # a classmethod is a function that has an implicit class pointer, taking subclassing into
                            # account
    "staticmethod",         # a staticmethod is a function that has neither a this or class pointer, but is associated
                            # with a specific class. Since it doesn't have a class pointer, it cannot be called in a
                            # virtual fashion
    "then", "elif",         # no extra language constructs like this
    "?",                    # no ternery operator or special optional syntax ala Swift
])
