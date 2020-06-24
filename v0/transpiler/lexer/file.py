from .line import Line


class File(object):

    def __init__(self, context, lines):
        self.__context = context
        width = max([len(line) for line in lines])
        self.lines = [Line(line, width, context.for_line_number(line_number, line))
                        for line_number, line in enumerate(lines)]
