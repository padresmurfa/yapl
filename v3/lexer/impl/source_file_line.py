

class SourceFileLine(object):

    def __init__(self, output_line_number, sha256, source_start_line_number, source_end_line_number, indent_level, dedented_line):
        assert (indent_level % 4 == 0), \
            ("expected indents in increments of 4 spaces for " + dedented_line)
        assert len(str(output_line_number)) <= 5
        assert len(str(source_start_line_number)) <= 5
        assert len(str(source_end_line_number)) <= 5
        indent_level = int(indent_level/4)
        assert len(str(indent_level)) <= 3
        self.output_line_number = output_line_number
        self.sha256 = sha256
        self.source_start_line_number = source_start_line_number
        self.source_end_line_number = source_end_line_number
        self.indent_level = indent_level
        self.dedented_line = dedented_line

    def write_line_to(self, output_file):
        if self.source_end_line_number == self.source_start_line_number:
            end = "      "
        else:
            end = " {: 5d}".format(self.source_end_line_number)
        l = "{: 5d} {} {: 5d}{} {: 3d} {}\n".format(
            self.output_line_number,
            self.sha256,
            self.source_start_line_number,
            end,
            self.indent_level,
            self.dedented_line
        )
        output_file.write(l)
