import os
import io
import yaml
import hashlib
import base64

from yapl.v4.lexer.shared.module_lines.manifest.actual_line import ActualLineBuilder
from yapl.v4.lexer.shared.module_lines.manifest.base import ManifestBase


class ManifestBuilder(ManifestBase):

    def __init__(self, transpilation_directory, sha256):
        super().__init__(transpilation_directory, sha256)
        self._actual_lines = []
        self._actual_line_content = {}
        self._logical_lines = []
        self._logical_line_content = {}

    def parse(self):
        actual_line_number = 1
        with io.open(self._module_filename, "r") as i:
            self._actual_lines = []
            actual_line = i.readline()
            while actual_line:
                parsed = ActualLineBuilder.parse(actual_line_number, actual_line)
                if parsed is not None:
                    self._actual_lines.append(parsed)
                    self._actual_line_content[parsed.sha256] = parsed.content
                actual_line_number += 1
                actual_line = i.readline()
            logical_line_number = 1
            content_lines = []
            comment_lines = []
            for actual_line in self._actual_lines:
                if actual_line.is_comment_line:
                    comment_lines.append(actual_line)
                elif actual_line.has_line_continuation_marker:
                    content_lines.append(actual_line)
                else:
                    if content_lines:
                        content_lines.append(actual_line)
                    else:
                        content_lines = [ actual_line ]
                    self.__logical_line_from_actual_lines(logical_line_number, comment_lines, content_lines)
                    content_lines = []
                    comment_lines = []
                    logical_line_number = logical_line_number + 1

    def __logical_line_from_actual_lines(self, logical_line_number, comment_lines, actual_lines):

        def encode(content_string):
            content_binary = content_string.encode("utf-8")
            base64_encoded = base64.b64encode(content_binary)
            hex_encoded = base64_encoded.hex()
            return hex_encoded

        if (len(comment_lines) + len(actual_lines)) == 1:
            only_line = (comment_lines + actual_lines)[0]
            result = {
                "logical_line_number": logical_line_number,
                "indent_level": only_line.indent_level,
                "actual_line_number": only_line.actual_line_number,
                "sha256": only_line.sha256,
                "content": encode(only_line.content)
            }
        else:
            content = []
            for actual_line in actual_lines:
                # xcxc - separate this into a different step / concept
                # e.g. physical line, effective line, real line, atomic line, ...
                # each line can be tokenised atomically, if line continuation markers have
                # been resolved. but basically, we're not interested in lines that end with \
                if content and content[-1].endswith("\""):
                    j = self._join_strings(content[:-1], actual_line)
                    if j is not None:
                        content[-1] = j
                        continue
                c = self._actual_line_content[actual_line.sha256]
                if c.endswith("\\"):
                    c = c[:-1].rstrip()
                content.append(c)
            content = " ".join(content) + "\n"
            if comment_lines:
                content = ("\n".join([
                    self._actual_line_content[actual_line.sha256]
                    for actual_line in comment_lines
                ])) + "\n" + content
            h = hashlib.sha256()
            h.update(content.encode("utf-8"))
            sha256 = h.hexdigest()
            self._actual_line_content[sha256] = content
            actual_line_numbers = [actual_line.actual_line_number for actual_line in comment_lines] + [actual_line.actual_line_number for actual_line in actual_lines]
            result = {
                "logical_line_number": logical_line_number,
                "indent_level": actual_lines[0].indent_level,
                "actual_line_numbers": {
                    "first": actual_line_numbers[0],
                    "last": actual_line_numbers[-1],
                },
                "sha256": sha256,
                "content": encode(content)
            }
        self._logical_lines.append(result)
        self._logical_line_content[result["sha256"]] = result

    def __join_strings(self, l, r):
        r = r.lstrip()
        if l.endswith("\"\"\"") and r.startswith("\"\"\""):
            return l[-3] + "\n" + r[3:]
        if l.endswith("\"") and r.startswith("\""):
            return l[-1] + r[1:]
        return None

    def save(self):
        os.makedirs(self._actual_lines_directory, mode=0o777, exist_ok=True)
        os.makedirs(self._logical_lines_directory, mode=0o777, exist_ok=True)
        actual_lines_manifest = {
            "module": {
                "sha256": self._module_sha256
            },
            "actual_lines": [l.sha256 for l in self._actual_lines]
        }
        logical_lines_manifest = {
            "module": {
                "sha256": self._module_sha256
            },
            "logical_lines": [l["sha256"] for l in self._logical_lines]
        }
        with io.open(self._actual_lines_manifest, 'w') as manifest_file:
            yaml.safe_dump(actual_lines_manifest, manifest_file)
        for k, v in self._actual_line_content.items():
            filename = os.path.join(self._actual_lines_directory, k + ".txt")
            with io.open(filename, 'w') as manifest_file:
                manifest_file.write(v)
        with io.open(self._logical_lines_manifest, 'w') as manifest_file:
            yaml.safe_dump(logical_lines_manifest, manifest_file)
        for k, v in self._logical_line_content.items():
            filename = os.path.join(self._logical_lines_directory, k + ".yaml")
            with io.open(filename, 'w') as manifest_file:
                yaml.safe_dump(v, manifest_file)
