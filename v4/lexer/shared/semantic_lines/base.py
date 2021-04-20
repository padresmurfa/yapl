import os


class ManifestBase(object):

    def __init__(self, transpilation_directory, sha256):
        self._module_filename = os.path.join(transpilation_directory, "modules", sha256 + ".yapl")
        self._module_sha256 = sha256
        self._semantic_lines_directory = os.path.join(transpilation_directory, "semantic_lines", sha256)
        self._semantic_lines_manifest = os.path.join(self._semantic_lines_directory, "manifest.yaml")
