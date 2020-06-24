from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .curlies import CurlyOpen, CurlyClose
from .comment import Comment
from .assignment import Assignment
from .if_then_else import IfThenElse
from .while_loop import WhileLoop
from .return_value import ReturnValue


class BlockMissingOpeningCurly(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class BlockMissingClosingCurly(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class BlockUnexpectedToken(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class BlockDeclaration(object):

    def __init__(self, tokens, parent):
        CurlyOpen(tokens)
        self.parent = parent
        self.contents = []

    @classmethod
    def matches(cls, tokens):
        return CurlyOpen.matches(tokens)

    def gobble(self, tokens):
        # imported locally to prevent circular dependency during loading
        from .class_declaration import ClassDeclaration
        from .function_declaration import FunctionDeclaration
        if len(tokens) == 0:
            raise BlockMissingClosingCurly()
        elif CurlyClose.matches(tokens):
            CurlyClose(tokens)
            return self.parent
        elif IfThenElse.matches(tokens):
            if_then_else = IfThenElse(tokens, self)
            self.contents.append(if_then_else)
            return if_then_else
        elif WhileLoop.matches(tokens):
            while_loop = WhileLoop(tokens, self)
            self.contents.append(while_loop)
            return while_loop
        elif FunctionDeclaration.matches(tokens):
            function_declaration = FunctionDeclaration(tokens, self)
            self.contents.append(function_declaration)
            return function_declaration
        elif Comment.matches(tokens):
            comment = Comment(self)
            self.contents.append(comment)
            return comment
        elif Assignment.matches(tokens):
            assignment = Assignment(tokens, self)
            self.contents.append(assignment)
            return assignment
        elif FunctionDeclaration.matches(tokens):
            function_declaration = FunctionDeclaration(tokens, self)
            self.contents.append(function_declaration)
            return function_declaration
        elif ClassDeclaration.matches(tokens):
            class_declaration = ClassDeclaration(tokens, self)
            self.contents.append(class_declaration)
            return class_declaration
        elif ReturnValue.matches(tokens):
            return_value = ReturnValue(tokens, self)
            self.contents.append(return_value)
            return return_value
        else:
            raise BlockUnexpectedToken()
