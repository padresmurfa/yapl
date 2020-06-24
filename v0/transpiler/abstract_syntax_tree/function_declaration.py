import re

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .function_arguments import FunctionArguments
from .parenthesis import ParenthesisClose, ParenthesisOpen
from .identifier import Identifier
from .block_declaration import BlockDeclaration
from .returns_declaration import ReturnsDeclaration
from .type_descriptor_separator import TypeDescriptorSeparator


class FunctionMissingIdentifier(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class FunctionUnexpectedToken(TranspilerSyntaxError):
    def __init__(self, offending_token):
        TranspilerSyntaxError.__init__(self, offending_token)


class FunctionMissingOpeningCurly(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class FunctionMissingClosingCurly(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class ClosureOver(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"control_flow.closure\(over\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class FunctionDeclaration(object):

    def __init__(self, tokens, parent):
        self.is_function = self.__pattern_function.match(tokens[0]) is not None
        self.is_closure = self.__pattern_closure.match(tokens[0]) is not None
        tokens.popleft()
        self.parent = parent
        self.ast_state = "UNIDENTIFIED"
        self.identifier = None
        self.arguments = None
        self.closure_over = None
        self.returns_name = None
        self.returns_type = None
        self.block = None

    __pattern_function = re.compile(
        r"\[\d+.\d+\]:"
        r"control_flow.function\(function\)"
    )

    __pattern_closure = re.compile(
        r"\[\d+.\d+\]:"
        r"control_flow.closure\(closure\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        is_function = cls.__pattern_function.match(tokens[0]) is not None
        is_closure = cls.__pattern_closure.match(tokens[0]) is not None
        return is_function or is_closure

    def gobble(self, tokens):
        # TODO: some types of comments are allowed in some of these states
        if self.ast_state == "UNIDENTIFIED":
            if len(tokens) == 0:
                raise FunctionMissingIdentifier()
            if Identifier.matches(tokens):
                self.identifier = Identifier(tokens)
                self.ast_state = "IDENTIFIED"
                return self
        elif self.ast_state == "IDENTIFIED":
            if len(tokens) == 0:
                raise FunctionMissingOpeningCurly()
            if ParenthesisOpen.matches(tokens):
                ParenthesisOpen(tokens)
                self.ast_state = "ARGUMENTS"
                self.arguments = FunctionArguments(self)
                return self.arguments
        elif self.ast_state == "ARGUMENTS":
            if ParenthesisClose.matches(tokens):
                ParenthesisClose(tokens)
                if self.is_closure:
                    self.ast_state = "CLOSURE_OVER"
                else:
                    self.ast_state = "RETURNS"
                return self
        elif self.ast_state == "CLOSURE_OVER":
            if ClosureOver.matches(tokens):
                ClosureOver(tokens)
                self.ast_state = "CLOSURE_OVER_ARGUMENTS"
                return self
        elif self.ast_state == "CLOSURE_OVER_ARGUMENTS":
            if ParenthesisOpen.matches(tokens):
                ParenthesisOpen(tokens)
                self.ast_state = "CLOSURE_OVER_OPENED"
                closure_over = FunctionArguments(self)
                self.closure_over = closure_over
                return closure_over
        elif self.ast_state == "CLOSURE_OVER_OPENED":
            if ParenthesisClose.matches(tokens):
                ParenthesisClose(tokens)
                self.ast_state = "RETURNS"
                return self
        elif self.ast_state == "RETURNS":
            if ReturnsDeclaration.matches(tokens):
                ReturnsDeclaration(tokens)
                self.ast_state = "RETURN_VALUE_DECLARATION"
                return self
            else:
                self.ast_state = "EXPECTING_BLOCK"
                return self
        elif self.ast_state == "EXPECTING_BLOCK":
            if BlockDeclaration.matches(tokens):
                block = BlockDeclaration(tokens, self)
                self.block = block
                self.ast_state = "BLOCK"
                return block
        elif self.ast_state == "RETURN_VALUE_DECLARATION":
            if Identifier.matches(tokens):
                self.returns_name = Identifier(tokens)
                self.ast_state = "RETURN_VALUE_DECLARATION_TYPE_DESCRIPTOR_SEPARATOR"
                return self
        elif self.ast_state == "RETURN_VALUE_DECLARATION_TYPE_DESCRIPTOR_SEPARATOR":
            if TypeDescriptorSeparator.matches(tokens):
                TypeDescriptorSeparator(tokens)
                self.ast_state = "RETURN_VALUE_DECLARATION_TYPE_DESCRIPTOR"
                return self
        elif self.ast_state == "RETURN_VALUE_DECLARATION_TYPE_DESCRIPTOR":
            if Identifier.matches(tokens):
                self.returns_type = Identifier(tokens)
                self.ast_state = "EXPECTING_BLOCK"
                return self
        elif self.ast_state == "BLOCK":
            return self.parent
        raise FunctionUnexpectedToken(tokens[0])
