import re

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .identifier import Identifier
from .literal import Literal
from .list_separator import ListSeparator
from .parenthesis import ParenthesisClose
from .assignment_operator import ImmutableAssignmentOperator
from .type_descriptor_separator import TypeDescriptorSeparator


class FunctionArgumentUnexpectedToken(TranspilerSyntaxError):
    def __init__(self, offending_token):
        TranspilerSyntaxError.__init__(self, offending_token)


class FunctionArgumentsUnexpectedToken(TranspilerSyntaxError):
    def __init__(self, offending_token):
        TranspilerSyntaxError.__init__(self, offending_token)


class FunctionArgument(object):

    def __init__(self, tokens, parent):
        self.parent = parent
        self.argument_name = Identifier(tokens)
        self.argument_type = None
        self.default_value = None
        self.ast_state = "IDENTIFIED"

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return Identifier.matches(tokens)

    def gobble(self, tokens):
        if self.ast_state == "IDENTIFIED":
            if TypeDescriptorSeparator.matches(tokens):
                TypeDescriptorSeparator(tokens)
                self.ast_state = "UNTYPED"
                return self
        elif self.ast_state == "UNTYPED":
            if Identifier.matches(tokens):
                self.argument_type = Identifier(tokens)
                self.ast_state = "UNTEMPLATED"
                return self
        elif self.ast_state == "UNTEMPLATED":
            # TODO: read [..] section
            self.ast_state = "NODEFAULT"
            return self
        elif self.ast_state == "NODEFAULT":
            if len(tokens) == 0:
                return self.parent
            elif ParenthesisClose.matches(tokens):
                return self.parent
            elif ListSeparator.matches(tokens):
                return self.parent
            elif ImmutableAssignmentOperator.matches(tokens):
                ImmutableAssignmentOperator(tokens)
                self.default_value = Literal(tokens)
                # TODO: this can be more than a literal
                return self.parent
        raise FunctionArgumentUnexpectedToken(tokens[0])


class FunctionArguments(object):

    def __init__(self, parent):
        self.parent = parent
        self.arguments = []
        self.ast_state = "MIGHT_HAVE_AN_ARGUMENT"

    def gobble(self, tokens):
        if self.ast_state == "MIGHT_HAVE_AN_ARGUMENT":
            if ParenthesisClose.matches(tokens):
                return self.parent
            elif FunctionArgument.matches(tokens):
                self.ast_state = "HAS_AN_ARGUMENT"
                argument = FunctionArgument(tokens, self)
                self.arguments.append(argument)
                return argument
        elif self.ast_state == "HAS_AN_ARGUMENT":
            if ListSeparator.matches(tokens):
                self.ast_state = "MIGHT_HAVE_AN_ARGUMENT"
                ListSeparator(tokens)
                return self
            elif ParenthesisClose.matches(tokens):
                return self.parent

        raise FunctionArgumentsUnexpectedToken(tokens[0])
