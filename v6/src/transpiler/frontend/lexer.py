from transpiler.frontend.lexemes import ALL_LEXEME_TYPES, advance_offset, consume, EndOfLine

class LexicallyAnalyzedLine(object):

    def __init__(self, lexer, line_number, line):
        self.__lexer = lexer
        self.__line_number = line_number
        self.__line = line
        self.__tokens = []

    def clone(self):
        cloned_line = LexicallyAnalyzedLine(self.__lexer, self.__line_number, self.__line)
        cloned_line.__tokens = self.__tokens[:]
        return cloned_line

    def get_line_number(self):
        return self.__line_number

    def __str__(self):
        return "LexicallyAnalyzedLine, for line number {}, with content: \"{}\"".format(self.__line_number, self.__line)

    def analyze(self):
        offset = 0
        tokens = []
        stripped = self.__line.rstrip()
        while True:
            stripped, offset = advance_offset(stripped, stripped.lstrip(), offset)
            # TODO: multi-line quoted string
            for lexeme_type in ALL_LEXEME_TYPES:
                consume = getattr(lexeme_type, "consume")
                stripped, offset = consume(tokens, stripped, offset)
            if len(stripped) > 0:
                continue
            break
        def decorate_token(token):
            token.set_lexical_line(self)
            return token
        assert tokens, "expected to have some tokens"
        self.__tokens = [ decorate_token(token) for token in tokens ]

    def peek_tokens(self):
        return self.__tokens

    def peek_leading_token(self):
        if not self.__tokens:
            eol = EndOfLine(len(self.__line))
            eol.set_lexical_line(self)
            return eol
        return self.__tokens[0]

    def pop_leading_token(self):
        leading_token = self.__tokens[0]
        self.__tokens = self.__tokens[1:]
        return leading_token

    def consume(self, leading_token):
        result = self.clone()
        popped_leading_token = result.pop_leading_token()
        assert leading_token is popped_leading_token, "expected the leading token to be the one provided ({}), not {}".format(str(leading_token), str(popped_leading_token))
        return result

class Lexer(object):

    def __init__(self):
        self.__next_line_number = 1

    def analyze_line(self, line):
        line_number = self.__next_line_number
        analyzed_line = LexicallyAnalyzedLine(self, line_number, line)
        analyzed_line.analyze()
        self.__next_line_number += 1
        return analyzed_line
