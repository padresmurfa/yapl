import io

class FileReader(object):

    def __init__(self, absolute_file_name):
        self.absolute_file_name = absolute_file_name

    def read_lines(self):
        last_line_was_empty = False
        with io.open(self.absolute_file_name) as f:
            for line in f.readlines():
                rstripped_line = line.rstrip()
                last_line_was_empty = rstripped_line == ""
                yield rstripped_line
