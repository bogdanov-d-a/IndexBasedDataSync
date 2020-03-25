# Untested!
import ed_ibds.ram_file_tree


def hash_dump_ram_file_tree(file_path, trim_length, separator='/'):
    input_ = codecs.open(file_path, 'r', 'utf-8-sig')
    data = ed_ibds.ram_file_tree.RamFileTreeDirectory('')

    for line in input_.readlines():
        data.add_file_path(line[trim_length:-1].split(separator))

    input_.close()
    return data


def sha256_dump_ram_file_tree(file_path):
    return hash_dump_ram_file_tree(file_path, 66)


def md5summer_dump_ram_file_tree(file_path):
    return hash_dump_ram_file_tree(file_path, 34)
