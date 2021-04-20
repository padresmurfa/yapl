import hashlib


class ActualLineBuilder(object):

    def __init__(self, actual_line_number, indent_level, sha256, content):
        self.actual_line_number = actual_line_number
        self.indent_level = indent_level
        self.sha256 = sha256
        self.has_line_continuation_marker = content.endswith("\\")
        self.is_comment_line = content.startswith("--")
        if self.has_line_continuation_marker:
            content = content[:-1].rstrip()
        self.content = content

    @staticmethod
    def parse(actual_line_number, actual_line):
        actual_line = actual_line.replace("\t", "    ").rstrip()
        if not actual_line:
            return None
        actual_line_without_indent = actual_line.lstrip()
        indentation = len(actual_line) - len(actual_line_without_indent)
        if actual_line_without_indent.startswith("---"):
            if not actual_line_without_indent.replace("-", ""):
                actual_line_without_indent = "---"
        h = hashlib.sha256()
        h.update(actual_line_without_indent.encode("utf-8"))
        sha256 = h.hexdigest()
        indent_level = int(indentation / 4)
        remaining_indent = indentation % 4
        if remaining_indent > 0:
            actual_line_without_indent = (" " * remaining_indent) + actual_line_without_indent
        return ActualLineBuilder(
            actual_line_number,
            indent_level,
            sha256,
            actual_line_without_indent
        )
