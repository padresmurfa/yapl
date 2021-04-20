import io
import os
import yaml
from yapl.v4.lexer.shared.tokenized_lines.base import ManifestBase



class TokenizedLinesManifestReader(object):

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


class TokenizedLine(object):

    def __init__(self, contents):
        self._contents = contents

    def sha256(self):
        return self._contents["sha256"]

    def tokens(self):
        return self._contents["tokens"]


class TokenizedLineReader(object):

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
        return TokenizedLine(self._manifest_contents)


class TokenizedLinesManifestReader(TokenizedLinesManifestReader):

    def __init__(self, module_sha256, manifest_filename):
        super().__init__(module_sha256, manifest_filename, "tokenized_lines")

    def lines(self):
        for line_sha in self._line_shas:
            yield TokenizedLineReader(line_sha, self._filename_of_line(line_sha, ".yaml")).contents()


class ManifestReader(ManifestBase):

    def __init__(self, transpilation_directory, sha256):
        super().__init__(transpilation_directory, sha256)
        self._lines = None

    def tokenized_lines(self):
        if self._lines is None:
            self._lines = TokenizedLinesManifestReader(
                self._module_sha256,
                self._tokenized_lines_manifest
            )
        for line in self._lines.lines():
            yield line
