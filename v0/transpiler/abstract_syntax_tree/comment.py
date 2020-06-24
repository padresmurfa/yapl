import re
import base64

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError


class CommentUnexpectedToken(TranspilerSyntaxError):
    def __init__(self, offending_token):
        TranspilerSyntaxError.__init__(self, offending_token)


class SingleLineComment(object):

    def __init__(self, tokens):
        match = self.__pattern.match(tokens.popleft())
        value = match.group("comment")
        self.comment = base64.b64decode(value)

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"comments.single_line\((?P<comment>[^\)]+)\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class OldSchoolComment(object):

    def __init__(self, tokens):
        match = self.__pattern.match(tokens.popleft())
        value = match.group("comment")
        self.comment = base64.b64decode(value)

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"comments.old_school\((?P<comment>[^\)]+)\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class Comment(object):

    def __init__(self, parent):
        self.parent = parent
        self.lines = []

    @classmethod
    def matches(cls, tokens):
        if SingleLineComment.matches(tokens):
            return True
        if OldSchoolComment.matches(tokens):
            return True
        return False

    def gobble(self, tokens):
        if SingleLineComment.matches(tokens):
            self.lines = [ SingleLineComment(tokens) ]
            return self.parent
        if OldSchoolComment.matches(tokens):
            self.lines = [ OldSchoolComment(tokens) ]
            return self.parent
        raise CommentUnexpectedToken(tokens[0])
