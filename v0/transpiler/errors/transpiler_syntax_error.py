class TranspilerSyntaxError(Exception):

    def __init__(self, offending_token):
        self.offending_token = offending_token
