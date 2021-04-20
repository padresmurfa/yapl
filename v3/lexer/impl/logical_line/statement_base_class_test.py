import unittest
from impl.logical_line.statement_base_class import StatementBaseClass


class RealizedStatementBaseClass(StatementBaseClass):
    def __init__(self, prefix, start_token, stop_token):
        super().__init__(prefix, start_token, stop_token)

    @classmethod
    def get_start_token(cls):
        raise NotImplementedError()

    @classmethod
    def may_contain_text_in_first_line(cls):
        raise NotImplementedError()

    def combine(self):
        raise NotImplementedError()


class TestStatementBaseClass(unittest.TestCase):
    """
    Unit test suite for StatementBaseClass
    """

