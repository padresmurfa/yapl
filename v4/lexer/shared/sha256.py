import io
import hashlib


def calculate_sha256_of_file(filename):
    sha256_hash = hashlib.sha256()
    with io.open(filename, "rb") as f:
        def read_block():
            return f.read(100 * 1024)
        for bytes in iter(read_block, b""):
            sha256_hash.update(bytes)
    return sha256_hash.hexdigest()


def calculate_sha256_of_string(s):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(s.encode("UTF-8"))
    return sha256_hash.hexdigest()
