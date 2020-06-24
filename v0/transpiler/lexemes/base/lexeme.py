import re

from .registry.lexeme_registry import LexemeRegistry


class Lexeme(object):

    def __init__(self, context, lexeme):
        self.__len = len(lexeme)
        self.__context = context.set_length(self.__len)
        self.__next_context = context.advance_character_position(self.__len)
        self.__lexeme = lexeme

    def next_context(self):
        return self.__next_context

    def remainder(self, whole):
        return whole[self.__len:]

    @classmethod
    def precedence(cls):
        return 0

    def __repr__(self):
        return "(type={}, context={})".format(type(self).__name__, self.__context)

    def to_intermediate_repr(self):
        return "{}".format(self.lexeme_id)

    @classmethod
    def register(cls):
        LexemeRegistry.register(cls)

    @staticmethod
    def splits_identifier(first, second):
        if not Lexeme.ends_with_identifier_character(first):
            return False
        if not Lexeme.starts_with_identifier_character(second):
            return False
        return True

    @staticmethod
    def starts_with_identifier_character(s):
        if len(s) == 0:
            return False
        regex_identifier_character = r"[a-zA-Z0-9_]"
        x = re.search(regex_identifier_character, s[0])
        return x is not None

    @staticmethod
    def ends_with_identifier_character(s):
        if len(s) == 0:
            return False
        regex_identifier_character = r"[a-zA-Z0-9_]"
        x = re.search(regex_identifier_character, s[-1])
        return x is not None
