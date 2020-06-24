import re

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .module_declaration import ModuleDeclaration
from .process_declaration import ProcessDeclaration


class FileUnexpectedToken(TranspilerSyntaxError):
    def __init__(self, offending_token):
        TranspilerSyntaxError.__init__(self, offending_token)


class FileMayContainOnlyOneShebang(TranspilerSyntaxError):
    def __init__(self, offending_token):
        TranspilerSyntaxError.__init__(self, offending_token)


class Shebang(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"shebangs\.shebang\([^\)]+\)")

    def spew(self, output):
        output("#!/usr/bin/env python3\n\n")

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class File(object):

    def __init__(self, filename):
        self.filename = filename
        self.shebang = None
        self.contents = []

    def gobble(self, tokens):
        if Shebang.matches(tokens):
            if self.shebang is not None:
                raise FileMayContainOnlyOneShebang(tokens[0])
            self.shebang = Shebang(tokens)
            self.contents.append(self.shebang)
            return self

        # TODO: Files may have comments

        elif ModuleDeclaration.matches(tokens):
            module = ModuleDeclaration(tokens, self)
            self.contents.append(module)
            return module

        elif ProcessDeclaration.matches(tokens):
            process = ProcessDeclaration(tokens, self)
            self.contents.append(process)
            return process

        elif len(tokens) == 0:
            return None

        else:
            raise FileUnexpectedToken(tokens[0])
