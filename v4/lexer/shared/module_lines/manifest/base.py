import os


class ManifestBase(object):

    def __init__(self, transpilation_directory, sha256):
        self._module_filename = os.path.join(transpilation_directory, "modules", sha256 + ".yapl")
        self._module_sha256 = sha256
        self._module_lines_directory = os.path.join(transpilation_directory, "module_lines", sha256)
        self._actual_lines_directory = os.path.join(self._module_lines_directory, "actual")
        self._actual_lines_manifest = os.path.join(self._actual_lines_directory, "manifest.yaml")
        self._logical_lines_directory = os.path.join(self._module_lines_directory, "logical")
        self._logical_lines_manifest = os.path.join(self._logical_lines_directory, "manifest.yaml")
