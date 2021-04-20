import os


class ManifestBase(object):

    def __init__(self, transpilation_directory, sha256):
        self._module_filename = os.path.join(transpilation_directory, "modules", sha256 + ".yapl")
        self._module_sha256 = sha256
        self._tokenized_lines_directory = os.path.join(transpilation_directory, "tokenized_lines", sha256)
        self._tokenized_lines_manifest = os.path.join(self._tokenized_lines_directory, "manifest.yaml")
