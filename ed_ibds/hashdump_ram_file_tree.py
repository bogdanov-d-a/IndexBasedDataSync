# Untested!
import codecs
from . import ram_file_tree


def hash_dump_ram_file_tree(file_path, trim_length, separator='/'):
    with codecs.open(file_path, 'r', 'utf-8-sig') as input_:
        data = ram_file_tree.Directory('')

        for line in input_.readlines():
            data.add_file_path(line[trim_length:-1].split(separator))

        return data


def sha256_dump_ram_file_tree(file_path):
    return hash_dump_ram_file_tree(file_path, 66)


def md5summer_dump_ram_file_tree(file_path):
    return hash_dump_ram_file_tree(file_path, 34)
