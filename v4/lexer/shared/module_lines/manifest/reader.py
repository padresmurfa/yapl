import io
import codecs
import os
import yaml
from yapl.v4.lexer.shared.module_lines.manifest.base import ManifestBase


class LinesManifestReader(object):

    def __init__(self, module_sha256, manifest_filename, lines_name):
        self._module_sha256 = module_sha256
        self._manifest_filename = manifest_filename
        self._manifest_directory = os.path.dirname(manifest_filename)
        with io.open(manifest_filename, 'r') as manifest_file:
            contents = yaml.safe_load(manifest_file)
            assert contents["module"]["sha256"] == module_sha256, \
                "Expected the sha256 of the manifest.yaml file to match the module sha256"
            self._line_shas = contents[lines_name]

    def __len__(self):
        return len(self._line_shas)

    def _filename_of_line(self, line_sha256, extension):
        if not extension.startswith("."):
            extension = "." + extension
        return os.path.join(self._manifest_directory, line_sha256) + extension


class ActualLineReader(object):

    def __init__(self, sha, filename):
        self._sha = sha
        self._filename = filename
        self._contents = None

    def contents(self):
        if self._contents is None:
            with io.open(self._filename, "r") as file:
                self._contents = file.read()
        return self._contents


class ActualLinesManifestReader(LinesManifestReader):

    def __init__(self, module_sha256, manifest_filename):
        super().__init__(module_sha256, manifest_filename, "actual_lines")

    def lines(self):
        for line_sha in self._line_shas:
            yield ActualLineReader(line_sha, self._filename_of_line(line_sha, ".txt")).contents()


class LogicalLine(object):

    def __init__(self, contents):
        self._contents = contents

    def sha256(self):
        return self._contents["sha256"]

    def indent_level(self):
        return self._contents["indent_level"]

    def logical_line_number(self):
        return self._contents["logical_line_number"]

    def actual_line_numbers(self):
        if "actual_line_number" in self._contents:
            aln = self._contents["actual_line_number"]
            return aln, aln
        else:
            alns = self._contents["actual_line_numbers"]
            return alns["first"], alns["last"]

    def content(self):
        def decode(hex_string):
            base64_encoded = codecs.decode(hex_string, "hex")
            content_binary = codecs.decode(base64_encoded, "base64")
            content_string = content_binary.decode("utf-8")
            return content_string
        return decode(self._contents["content"])


class LogicalLineReader(object):

    def __init__(self, sha, filename):
        self._sha = sha
        self._filename = filename
        self._manifest_contents = None

    def contents(self):
        if self._manifest_contents is None:
            with io.open(self._filename, 'r') as manifest_file:
                self._manifest_contents = yaml.safe_load(manifest_file)
                assert self._manifest_contents["sha256"] == self._sha, \
                    "Expected the sha256 of the line.yaml file to match the line sha256"
        return LogicalLine(self._manifest_contents)


class LogicalLinesManifestReader(LinesManifestReader):

    def __init__(self, module_sha256, manifest_filename):
        super().__init__(module_sha256, manifest_filename, "logical_lines")

    def lines(self):
        for line_sha in self._line_shas:
            yield LogicalLineReader(line_sha, self._filename_of_line(line_sha, ".yaml")).contents()


class ManifestReader(ManifestBase):

    def __init__(self, transpilation_directory, sha256):
        super().__init__(transpilation_directory, sha256)
        self._actual_lines = None
        self._logical_lines = None

    def actual_lines(self):
        if self._actual_lines is None:
            self._actual_lines = ActualLinesManifestReader(
                self._module_sha256,
                self._actual_lines_manifest
            )
        for line in self._actual_lines.lines():
            yield line

    def logical_lines(self):
        if self._logical_lines is None:
            self._logical_lines = LogicalLinesManifestReader(
                self._module_sha256,
                self._logical_lines_manifest
            )
        for line in self._logical_lines.lines():
            yield line
