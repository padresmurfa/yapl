from .lexer import Lexer


class Line(object):

    def __init__(self, text, width, context):
        self.__text = text
        self.__context = context
        self.lexemes = Lexer(context).lexemes_from_line(text)
        self.__width = width

    def __repr__(self):
        text = self.__text.rstrip().ljust(self.__width)
        return "{} | {} | {}".format(self.__context.get_line_number(), text, self.lexemes)
