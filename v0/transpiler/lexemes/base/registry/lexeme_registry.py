import inspect
import sys


class LexemeRegistry:

    modules = set()
    lexemes = []

    @classmethod
    def register(cls, lexeme):
        if lexeme in cls.lexemes:
            return
        if not hasattr(lexeme, "try_extract"):
            print("ERROR: try_extract not found for lexeme: " + str(lexeme))
            return
        cls.lexemes.append(lexeme)

    @classmethod
    def register_all_lexemes_in_module(cls, module_name):
        if module_name in cls.modules:
            return
        cls.modules.add(module_name)

        module = sys.modules[module_name]
        for name, lexeme in inspect.getmembers(module):
            if inspect.isclass(lexeme):
                if issubclass(lexeme, Lexeme):
                    if lexeme.__module__ == module_name: # prevent imports from being slurped in
                        cls.lexemes.append(lexeme)

    @classmethod
    def initialize(cls):
        cls.lexemes.sort(key=lambda lexeme: lexeme.precedence(), reverse=True)
