import re

from transpiler.errors.transpiler_syntax_error import TranspilerSyntaxError

from .parenthesis import ParenthesisOpen, ParenthesisClose
from .boolean_expression import BooleanExpression


class WhileLoopUnexpectedToken(TranspilerSyntaxError):
    def __init__(self):
        TranspilerSyntaxError.__init__(self, None)


class WhileLoop(object):

    def __init__(self, tokens, parent):
        tokens.popleft()
        self.parent = parent
        self.ast_state = "EXPECTING_EXPRESSION"
        self.expression = None
        self.block = None

    __pattern = re.compile(
        r"\[\d+.\d+\]:"
        r"control_flow.do_while_loop\(while\)"
    )

    @classmethod
    def matches(cls, tokens):
        if len(tokens) < 1:
            return False
        return cls.__pattern.match(tokens[0]) is not None

    def gobble(self, tokens):
        from .block_declaration import BlockDeclaration
        if self.ast_state == "EXPECTING_EXPRESSION":
            if ParenthesisOpen.matches(tokens):
                ParenthesisOpen(tokens)
                expression = BooleanExpression(tokens, self)
                self.expression = expression
                self.ast_state = "EXPECTING_CLOSE_PARENTHESIS"
                return expression
        elif self.ast_state == "EXPECTING_CLOSE_PARENTHESIS":
            if ParenthesisClose.matches(tokens):
                ParenthesisClose(tokens)
                self.ast_state = "EXPECTING_BLOCK"
                return self
        elif self.ast_state == "EXPECTING_BLOCK":
            if BlockDeclaration.matches(tokens):
                block = BlockDeclaration(tokens, self)
                self.block = block
                self.ast_state = "BLOCK"
                return block
        elif self.ast_state == "BLOCK":
            return self.parent
        raise WhileLoopUnexpectedToken()
