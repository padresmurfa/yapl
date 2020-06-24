import base64

from .base.lexeme import Lexeme
from .operators.arithmetic import ArithmeticOperatorLexeme


class SingleLineCommentLexeme(Lexeme):

    lexeme_id = "comments.single_line"

    def __init__(self, context, lexeme, comment):
        Lexeme.__init__(self, context, lexeme)
        self.__comment = comment

    def __repr__(self):
        return Lexeme.__repr__(self)[:-1] + ", comment=\"" + self.__comment + "\")"

    def to_intermediate_repr(self):
        comment_as_bytes = base64.b64encode(self.__comment.encode("utf-8"))
        comment_as_string = str(comment_as_bytes, "utf-8")
        return "{}({})".format(self.lexeme_id, comment_as_string)

    @classmethod
    def precedence(cls):
        return 1 + ArithmeticOperatorLexeme.PRECEDENCE

    @staticmethod
    def try_extract(source, context):
        if source.startswith("//"):
            lexeme = SingleLineCommentLexeme(context, source, source[2:])
            return lexeme, lexeme.remainder(source), lexeme.next_context()
        return None, source, context


SingleLineCommentLexeme.register()
