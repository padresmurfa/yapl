import base64

from .base.lexeme import Lexeme


class ShebangLexeme(Lexeme):

    lexeme_id = "shebangs.shebang"

    def __init__(self, context, lexeme, command):
        Lexeme.__init__(self, context, lexeme)
        self.__command = command

    def __repr__(self):
        return Lexeme.__repr__(self)[:-1] + ", command=\"" + self.__command + "\")"

    def to_intermediate_repr(self):
        command_as_bytes = base64.b64encode(self.__command.encode("utf-8"))
        command_as_string = str(command_as_bytes, "utf-8")
        return "{}({})".format(self.lexeme_id, command_as_string)

    @staticmethod
    def try_extract(source, context):
        if source.startswith("#!"):
            lexeme = ShebangLexeme(context, source, source[2:])
            return lexeme, lexeme.remainder(source), lexeme.next_context()
        return None, source, context


ShebangLexeme.register()
