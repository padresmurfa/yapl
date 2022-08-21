import abc

from transpiler.frontend.lexer import LexicallyAnalyzedLine

class ContextBaseClass(metaclass=abc.ABCMeta):
    """
        Abstract base class used by all Context objects
    """

    def __init__(self, job, parent_context, component, indentation_level):
        """
            initializes this Context base-class

            'job' is the transpilation Job that hosts the context, or None, if we should ask the parent for this
            'parent_context' is the Context that is parent to this Context, or None, if we are topmost
            'component' is a constant string used for message-grouping that identifies what kind of Context this is.
        """
        self.__parent_context = parent_context
        self.__job = job
        self.__contents = []
        self.__component = component
        self.__indentation_level = indentation_level

    def get_indentation_level(self):
        """
            retrieves the indentation level that this context is declared on
        """
        return self.__indentation_level

    def get_contents(self):
        """
            Retreives the internal contents that have been pushed to this Context, which may be either
            lexically-analyzed-lines or sub-Contexts in their own right.
        """
        return self.__contents

    def get_parent_context(self):
        """
            Retrieves the parent context of this Context, or None for the top-most Context.
        """
        return self.__parent_context

    def get_job(self):
        """
            retrieves the transpiler Job that this Context is part of
        """
        if self.__job is None:
            self.__job = self.__parent_context.get_job()
        return self.__job

    def push_lexer_line(self, lexer_line):
        """
            pushes a lexically-analyzed-line to the end of this Context's contents list.
        """
        self.__contents.append(lexer_line)

    def peek_lexer_line(self):
        """
            peeks at the last lexically-analyzed-line that was added to this Context, and if such a line
            still exists and isn't a sub-Context, then it is returned without popping it. Otherwise the
            return value is None
        """
        if len(self.__contents) == 0:
            return None
        result = self.__contents[-1]
        if not isinstance(result, LexicallyAnalyzedLine):
            return None
        return result

    def pop_lexer_line(self):
        """
            pops the last lexically-analyzed-line that was added to this Context from its internal contents,
            returing it.
        """
        result = self.__contents[-1]
        del self.__contents[-1]
        return result

    def push_child_context(self, child_context):
        """
            Pushes a child-context ('child_context') onto the job's ContextStack, and adds it to our contents
        """
        self.__contents.append(child_context)
        self.get_job().get_context_stack().push_context(child_context)
        
    def pop_to_parent_context(self):
        """
            pops this Context of the job's ContextStack, returning the parent Context, or None if we're at the
            top of the ContextStack
        """
        context_stack = self.get_job().get_context_stack()
        if context_stack.is_empty():
            parent = None
        else:
            parent = context_stack.current_context().get_parent_context()
        context_stack.pop_context(self)
        return parent

    def error(self, error_code, message, location):
        """
            forwards an error message, with an error code (string), and a location-of-origin, to the job
        """
        self.get_job().error(self.__component, error_code, message, location, self.get_fully_qualified_name())

    def trace(self, message, location):
        """
            forwards a trace message, with a location-of-origin, to the job
        """
        self.get_job().trace(self.__component, message, location, self.get_fully_qualified_name())

    def maybe_pop_prefix_comments_at_offset(self, offset):
        """
            Helper function to pop a prefix-comment off the contents of this context, if one is to be found

            'offset' is the offset at which we expect to find the prefix comment. If this does not match, then
            the comment will not be popped.

            returns a list of the comment lines popped, in the order they appear in the source file.
        """
        prefix_comments_in_reverse_order = []
        while True:
            lexer_line = self.peek_lexer_line()
            if lexer_line is not None:
                leading_token = lexer_line.peek_leading_token()
                if leading_token.get_offset() == offset and leading_token.is_comment():
                    prefix_comments_in_reverse_order.append(lexer_line)
                    self.pop_lexer_line()
                    continue
            break
        prefix_comments_in_reverse_order.reverse()
        return prefix_comments_in_reverse_order

    @abc.abstractmethod
    def process_line(self, lexer_line):
        """
            called by the framework to process a line
        """
        pass

    def process_end_of_context(self, lexer_line):
        """
            called by the framework on the current Context when the end-of-context is reached unceremoniously, e.g. due to the start of a new
            less-indented context.
        """
        self.trace("end-of-context encountered", lexer_line)

    def process_end_of_file(self):
        """
            called by the framework on the current Context when the end-of-file is reached. The Context should pop itself from the stack,
            and forward the process_end_of_file call to its parent context, if any.
        """
        self.pop_to_parent_context().process_end_of_file()
        

    def validate_contents(self):
        """
            called by the framework after processing the file, to validate the overall contents of the context
        """
        contents = self.get_contents()
        for content in contents:
            if not isinstance(content, ContextBaseClass):
                self.trace("validating contexts: context not fully processed ({})".format(content), content)
            else:
                content.validate_contents()

    def get_fully_qualified_name(self):
        """
            retrieves the fully-qualified name of this context
        """
        assert self.__parent_context is not None, "root-level contexts must override get_fully_qualified_name()"
        return self.__parent_context.get_fully_qualified_name() + "." + self.get_name()

    @abc.abstractmethod
    def get_name(self):
        """
            retrieves the name of this context
        """
        pass
