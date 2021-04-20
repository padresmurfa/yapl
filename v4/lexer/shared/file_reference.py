import os
import collections
from yapl.v4.lexer.shared.sha256 import calculate_sha256_of_file

FileReference = collections.namedtuple("FileReference", ["root_directory", "relative_pathname", "absolute_pathname", "sha256"])


def to_file_reference(root_directory, full_filename):
    absolute = os.path.abspath(full_filename)
    relative = os.path.relpath(absolute, root_directory)
    sha256 = calculate_sha256_of_file(absolute)
    return FileReference(root_directory, relative, absolute, sha256)


