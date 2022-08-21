import re
import sys

def advance_offset(input, output, current_offset):
    return output, current_offset + len(input) - len(output)

def join(*patterns):
    parenthesized = []
    for pattern in patterns:
        parenthesized.append("(" + pattern + ")")
    joined = "|".join(parenthesized)
    return "^(" + joined + ")"


def join_words(*patterns):
    parenthesized = []
    for pattern in patterns:
        parenthesized.append("(" + pattern + "$)")
        parenthesized.append("(" + pattern + "\\b)")
    joined = "|".join(parenthesized)
    return "^(" + joined + ")"

def consume(tokens, input, pattern, constructor, offset):
    try:
        token_result = re.search(pattern, input)
    except re.error:
        _type, _value, _traceback = sys.exc_info()
        print("INTERNAL ERROR: bad regular expression")
        print("pattern: " + pattern)
        if _value.pos:
            print("         " + ((_value.pos -1) * "-") + "⬆")
        raise
    if token_result:
        token = token_result[0].rstrip()
        tokens.append(constructor(token, offset))
        output = input[len(token):]
    else:
        output = input
    return advance_offset(input, output, offset)

def consume_string(tokens, input, delimiter, constructor, offset):
    next_quote = 1
    if input.startswith(delimiter):
        while True:
            if next_quote >= len(input):
                break
            tmp = input.find(delimiter, next_quote)
            if tmp == -1:
                break
            if input[tmp - 1] == '\\':
                next_quote = tmp + 1
                continue
            quoted_string = input[1:next_quote]
            quoted_string = quoted_string.replace("\\\"", '"')
            quoted_string = quoted_string.replace("\\\'", "'")
            quoted_string = quoted_string.replace("\\\\", "\\")
            quoted_string = quoted_string.replace("\\r", "\r")
            quoted_string = quoted_string.replace("\\n", "\n")
            quoted_string = quoted_string.replace("\\t", "\t")
            # TODO: \uFFFF \UFFFFFFFF \xFF
            tokens.append(constructor(quoted_string))
            return advance_offset(input, input[next_quote+1:], offset)
    return input, offset

class Lexeme(object):

    def __init__(self, value, offset):
        self.__value = value
        self.__offset = offset
        self.__lexical_line = None

    def get_printable_value(self):
        return "[type={}, value=\"{}\"]".format(
            type(self).__name__,
            self.__value
        )

    def __str__(self):
        return "Lexeme of type {}, with value={}".format(
            type(self).__name__,
            self.__value
        )

    def get_lexical_line(self):
        return self.__lexical_line

    def set_lexical_line(self, lexical_line):
        self.__lexical_line = lexical_line

    def get_offset(self):
        return self.__offset

    def get_lexeme_value(self):
        return self.__value

    def is_callable(self, value=None):
        if not isinstance(self, Callable):
            return False
        if value is not None:
            if value != self.__value:
                return False
        return True

    def is_callable_segment(self, value=None):
        if not isinstance(self, CallableSegment):
            return False
        if value is not None:
            if value != self.__value:
                return False
        return True

    def is_keyword(self, value=None):
        if not isinstance(self, Keyword):
            return False
        if value is not None:
            if value != self.__value:
                return False
        return True

    def is_class_facet_type(self, value=None):
        if not isinstance(self, ClassFacetType):
            return False
        if value is not None:
            if value != self.__value:
                return False
        return True

    def is_visibility_level(self, value=None):
        if not isinstance(self, VisibilityLevel):
            return False
        if value is not None:
            if value != self.__value:
                return False
        return True
    
    def is_end_of_line(self):
        return isinstance(self, EndOfLine)

    def is_comment(self):
        return isinstance(self, Comment) or isinstance(self, CommentHorizontalRule)

    def is_comment_horizontal_rule(self):
        return isinstance(self, CommentHorizontalRule)

    def is_empty_line(self):
        return isinstance(self, EmptyLine)

    def is_token(self):
        return isinstance(self, Token) or isinstance(self, QualifiedToken)

    def is_qualified_token(self):
        return isinstance(self, QualifiedToken)

    def is_symbol(self, value=None):
        if not (isinstance(self, TwoGlyphSymbol) or isinstance(self, SingleGlyphSymbol)):
            return False
        if value is not None:
            if value != self.__value:
                return False
        return True

class EmptyLine(Lexeme):

    def __init__(self, offset):
        Lexeme.__init__(self, "", offset)

    def get_printable_value(self):
        return "[type={}]".format(
            type(self).__name__
        )

    @staticmethod
    def consume(tokens, input, offset):
        if input == "":
            tokens.append(EmptyLine(offset))
        return input, offset

class EndOfLine(Lexeme):

    def __init__(self, offset):
        Lexeme.__init__(self, "", offset)

    def get_printable_value(self):
        return "[type={}]".format(
            type(self).__name__
        )

    @staticmethod
    def consume(tokens, input, offset):
        if input == "":
            tokens.append(EndOfLine(offset))
        return input, offset

class CommentHorizontalRule(Lexeme):

    def __init__(self, characters, offset):
        Lexeme.__init__(self, characters, offset)

    @staticmethod
    def consume(tokens, input, offset):
        pattern = "^(---+)$"
        return consume(tokens, input, pattern, CommentHorizontalRule, offset)

class Comment(Lexeme):

    def __init__(self, characters, offset):
        Lexeme.__init__(self, characters, offset)

    @staticmethod
    def consume(tokens, input, offset):
        pattern = "^(--.*)$"
        return consume(tokens, input, pattern, Comment, offset)

class QualifiedToken(Lexeme):

    def __init__(self, characters, offset):
        Lexeme.__init__(self, characters, offset)

    def is_valid_fully_qualified_token(self):
        value = self.get_lexeme_value()
        if "__" in value:
            return False
        if ".." in value:
            return False
        if value.endswith("_") or value.endswith("."):
            return False
        if len(value.split(".")) < 3:
            return False
        return True

    @staticmethod
    def consume(tokens, input, offset):
        pattern = r"^([a-z][a-z0-9_]+)\.([a-z][a-z0-9_\.]+)"
        return consume(tokens, input, pattern, QualifiedToken, offset)

class Token(Lexeme):

    def __init__(self, characters, offset):
        Lexeme.__init__(self, characters, offset)

    def is_valid_token(self):
        value = self.get_lexeme_value()
        if "__" in value:
            return False
        if value.endswith("_"):
            return False
        return True

    @staticmethod
    def consume(tokens, input, offset):
        pattern = "^([a-z][a-z0-9_]+)"
        return consume(tokens, input, pattern, Token, offset)

class TwoGlyphSymbol(Lexeme):

    def __init__(self, characters, offset):
        Lexeme.__init__(self, characters, offset)

    @staticmethod
    def consume(tokens, input, offset):
        pattern = join("==", "<=", ">=", "!=", ":=", r"\+=", "-=", r"\*=", "/=")
        return consume(tokens, input, pattern, TwoGlyphSymbol, offset)

class SingleGlyphSymbol(Lexeme):

    def __init__(self, characters, offset):
        Lexeme.__init__(self, characters, offset)

    @staticmethod
    def consume(tokens, input, offset):
        pattern = join(r"\(", r"\)", "<", ">", r"\+", "-", r"\*", "/", ":", r"\.")
        return consume(tokens, input, pattern, SingleGlyphSymbol, offset)

class Keyword(Lexeme):

    def __init__(self, characters, offset):
        Lexeme.__init__(self, characters, offset)

    @staticmethod
    def consume(tokens, input, offset):
        pattern = join_words(
            "module",
            "class"
        )
        return consume(tokens, input, pattern, Keyword, offset)

class ClassFacetType(Lexeme):

    def __init__(self, characters, offset):
        Lexeme.__init__(self, characters, offset)

    @staticmethod
    def consume(tokens, input, offset):
        pattern = join_words(
            "facet",
            "interface",
            "trait",
        )
        return consume(tokens, input, pattern, ClassFacetType, offset)

class Callable(Lexeme):

    def __init__(self, characters, offset):
        Lexeme.__init__(self, characters, offset)

    @staticmethod
    def consume(tokens, input, offset):
        pattern = join_words(
            "function", "generator", "constructor", "method", "getter", "setter", "closure"
        )
        return consume(tokens, input, pattern, Callable, offset)

class CallableSegment(Lexeme):

    def __init__(self, characters, offset):
        Lexeme.__init__(self, characters, offset)

    @staticmethod
    def consume(tokens, input, offset):
        pattern = join_words(
            "inputs", "returns", "errors", "code", "emits", "preconditions", "postconditions"
        )
        return consume(tokens, input, pattern, CallableSegment, offset)

class VisibilityLevel(Lexeme):

    def __init__(self, characters, offset):
        Lexeme.__init__(self, characters, offset)

    @staticmethod
    def consume(tokens, input, offset):
        pattern = join_words(
            "public", "private", "protected"
        )
        return consume(tokens, input, pattern, VisibilityLevel, offset)

class LiteralNumber(Lexeme):

    def __init__(self, token, offset):
        self.__token = token
        self.__offset = offset

    @staticmethod
    def consume(tokens, input, offset):
        pattern = r"^(([+-]?[0-9]+)(\.[0-9+])?([eE][+-]\d)?)"
        return consume(tokens, input, pattern, LiteralNumber, offset)

class LiteralBoolean(Lexeme):

    def __init__(self, token, offset):
        self.__token = token
        self.__offset = offset

    @staticmethod
    def consume(tokens, input, offset):
        pattern = join_words("true", "false")
        return consume(tokens, input, pattern, LiteralBoolean, offset)


class DoubleQuotedString(Lexeme):

    def __init__(self, token, offset):
        self.__token = token
        self.__offset = offset

    @staticmethod
    def consume(tokens, input, offset):
        return consume_string(tokens, input, '"', DoubleQuotedString, offset)

class SingleQuotedString(Lexeme):

    def __init__(self, token, offset):
        self.__token = token
        self.__offset = offset

    @staticmethod
    def consume(tokens, input, offset):
        return consume_string(tokens, input, '"', SingleQuotedString, offset)


ALL_LEXEME_TYPES = [
    EmptyLine,
    CommentHorizontalRule,
    Comment,
    DoubleQuotedString,
    SingleQuotedString,
    TwoGlyphSymbol,
    LiteralBoolean,
    Keyword,
    ClassFacetType,
    VisibilityLevel,
    Callable,
    CallableSegment,
    LiteralNumber,
    SingleGlyphSymbol,
    QualifiedToken,
    Token,
]
