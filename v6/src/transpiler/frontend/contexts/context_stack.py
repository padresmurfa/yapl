class Stack(object):
    """
        A Context Stack, used to represent the layers of context-sensitive parsers that process a YAPL file
    """

    def __init__(self):
        self.__stack = []

    def is_empty(self):
        """
            returns True, iff this stack is empty
        """
        return len(self.__stack) == 0

    def push_context(self, context):
        """
            Pushes 'context' to the end of the stack
        """
        self.__stack.append(context)

    def pop_context(self, context=None):
        """
            Pops the last context from our stack.
            
            'context' if provided, will be used to assert that the stack is as we expected it to be
        """
        current = self.__stack.pop()
        if context is not None:
            assert context == current, "expected {} to be the current context at this point in time".format(str(context))

    def current_context(self):
        """
            Gives a peek at the last Context on our stack
        """
        return self.__stack[-1]
