import hashlib
from . import standard_type_assertion


def read_in_chunks(file_object, chunk_size=1024):
    standard_type_assertion.assert_integer_gtz('chunk_size', chunk_size)

    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def sha1(file_name):
    standard_type_assertion.assert_string('file_name', file_name)

    sha1 = hashlib.sha1()

    with open(file_name, 'rb') as f:
        for chunk in read_in_chunks(f):
            sha1.update(chunk)

    return sha1.hexdigest()
