import copy


class Context(object):

    def __init__(self, filename):
        self.__parent = None
        self.__filename = filename
        self.__line_number = None
        self.__line = None
        self.__character_number = 0
        self.__length = 0

    def get_line_number(self):
        return self.__line_number

    def for_line_number(self, line_number, line):
        context = copy.copy(self)
        context.__parent = self
        context.__line_number = line_number
        context.__character_number = 0
        context.__line = line
        context.__length = 0
        return context

    def advance_character_position(self, advance):
        context = copy.copy(self)
        context.__character_number = context.__character_number + advance
        return context

    def set_length(self, length):
        context = copy.copy(self)
        context.__length = length
        return context

    def __repr__(self):
        if self.__length > 0:
            return "(line={}, chars={}..{})".format(self.__line_number, self.__character_number,
                                                    self.__character_number + self.__length)
        else:
            return "(line={}, char={})".format(self.__line_number, self.__character_number)


Context.EMPTY = Context(None)
