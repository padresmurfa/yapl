import re

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .parenthesis import ParenthesisOpen, ParenthesisClose
from .boolean_expression import BooleanExpression


class IfThenElseMissingConditionalExpression(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class IfThenElseMissingExecutionBlock(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class IfThenElseDanglingElse(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class IfThenElseUnexpectedToken(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class If(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"control_flow.if_then_else\(if\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class Else(object):

    def __init__(self, tokens):
        tokens.popleft()

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"control_flow.if_then_else\(else\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None


class IfThenElse(object):

    def __init__(self, tokens, parent):
        If(tokens)
        self.parent = parent
        self.ast_state = "CONDITIONAL_EXPRESSION_BEFORE_PARENTHESIS_OPEN"
        self.conditional_branches = []
        self.default_branch = None
        self.__conditional_expression = None

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 2:
            return False
        return If.matches(tokens)

    def gobble(self, tokens):
        from .block_declaration import BlockDeclaration
        # TODO: some types of comments are allowed in some of these states
        if self.ast_state == "CONDITIONAL_EXPRESSION_BEFORE_PARENTHESIS_OPEN":
            if ParenthesisOpen.matches(tokens):
                ParenthesisOpen(tokens)
                self.ast_state = "CONDITIONAL_EXPRESSION"
                return self
        elif self.ast_state == "CONDITIONAL_EXPRESSION":
            if len(tokens) == 0:
                raise IfThenElseMissingConditionalExpression()
            elif BooleanExpression.matches(tokens):
                self.ast_state = "CONDITIONAL_EXPRESSION_AFTER_PARENTHESIS_CLOSE"
                ce = BooleanExpression(tokens, self)
                self.__conditional_expression = ce
                return ce
        elif self.ast_state == "CONDITIONAL_EXPRESSION_AFTER_PARENTHESIS_CLOSE":
            if ParenthesisClose.matches(tokens):
                ParenthesisClose(tokens)
                self.ast_state = "CONDITIONAL_BLOCK"
                return self
        elif self.ast_state == "CONDITIONAL_BLOCK":
            if len(tokens) == 0:
                raise IfThenElseMissingExecutionBlock()
            elif BlockDeclaration.matches(tokens):
                conditional_block = BlockDeclaration(tokens, self)
                self.conditional_branches.append((self.__conditional_expression, conditional_block))
                self.__conditional_expression = None
                self.ast_state = "AFTER_CONDITIONAL_BLOCK"
                return conditional_block
        elif self.ast_state == "AFTER_CONDITIONAL_BLOCK":
            if len(tokens) == 0:
                return self.parent
            elif Else.matches(tokens):
                Else(tokens)
                if len(tokens) == 0:
                    raise IfThenElseDanglingElse()
                if If.matches(tokens):
                    self.ast_state = "CONDITIONAL_EXPRESSION"
                    return self
                elif BlockDeclaration.matches(tokens):
                    default_branch = BlockDeclaration(tokens, self)
                    self.default_branch = default_branch
                    self.ast_state = "AFTER_DEFAULT_BLOCK"
                    return default_branch
        elif self.ast_state == "AFTER_DEFAULT_BLOCK":
            return self.parent

        raise IfThenElseUnexpectedToken()