from collections import deque

from transpiler.lexer import Context as LexerContext, File as LexerFile

from .file import File


def dump_lines(lines):
    print("lines:")
    print("=================================")
    for line in lines:
        print(line)


class AbstractSyntaxTree(object):

    def parse(self, filename):
        with open(filename) as f:
            context = LexerContext(filename)
            file = LexerFile(context, f.readlines())

            # spew out debug output, representing the lexed file
            dump_lines(file.lines)

            # convert the lexemes into our internal format
            # TODO: you're not really leveraging regular expressions, so you might as well
            #       switch patterns, or reconsider how you leverage them.
            lexemes = deque(AbstractSyntaxTree.parse_file(file))

            current = File(filename)
            cutoff = 0
            while lexemes:
                state = ""
                if hasattr(current,"ast_state"):
                    state = ":" + current.ast_state
                print("[" + type(current).__name__ + state + "] <- " + str(lexemes[0]))
                try:
                    next = current.gobble(lexemes)
                except Exception as e:
                    print("remainder: " + str(lexemes))
                    raise e
                cutoff += 1
                if cutoff == 500:
                    break
                current = next

    @staticmethod
    def parse_file(file):
        for line_number, line in enumerate(file.lines):
            for lexeme_number, lexeme in enumerate(line.lexemes):
                location = "{}.{}".format(line_number + 1, lexeme_number)

                def add_location(s):
                    return "[{}]:{}".format(location, s)
                if isinstance(lexeme, str):
                    i = add_location("\"{}\"".format(lexeme))
                else:
                    i = add_location("{}".format(lexeme.to_intermediate_repr()))
                yield i
