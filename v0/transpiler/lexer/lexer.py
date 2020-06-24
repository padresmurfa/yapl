from transpiler.lexemes.base.registry.lexeme_registry import LexemeRegistry


class Lexer:

    def __init__(self, context):
        self.__context = context
        LexemeRegistry.initialize()

    def lexemes_from_line(self, line):
        lexemes = []
        remainder = line.rstrip()
        if len(remainder) == 0:
            return []

        current_context = self.__context
        while True:
            stripped = remainder.strip()
            advanced = len(remainder) - len(stripped)
            if advanced > 0:
                current_context = current_context.advance_character_position(advanced)
            remainder = stripped
            if len(remainder) == 0:
                break
            consumed = False
            for lexeme_type in LexemeRegistry.lexemes:
                method = getattr(lexeme_type, "try_extract")
                try:
                    lexeme, remainder, current_context = method(remainder, current_context)
                    if lexeme is not None:
                        lexemes.append(lexeme)
                        consumed = True
                        break
                except RuntimeError as e:
                    print("error: " + str(lexeme_type) + str(e))
            if not consumed:
                lexemes.append(remainder)
                remainder = ""
        return lexemes
