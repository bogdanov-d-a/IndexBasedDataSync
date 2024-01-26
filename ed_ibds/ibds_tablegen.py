from . import standard_type_assertion
from . import file_tree_snapshot
from . import ibds_utils


def indexes(index_list):
    standard_type_assertion.assert_list_pred('index_list', index_list, file_tree_snapshot.assert_index)
    table = {}

    paths = set()
    for index_main in index_list:
        paths |= index_main.getKeySet()

    for path in paths:
        table[path] = [None] * len(index_list)

    for path in table.keys():
        for index_index in range(len(index_list)):
            if index_list[index_index].hasData(path):
                table[path][index_index] = index_list[index_index].getData(path)

    return table


def index_files(index_file_list):
    standard_type_assertion.assert_list_pred('index_file_list', index_file_list, standard_type_assertion.assert_string)

    index_list = list(map(lambda path: file_tree_snapshot.load_index(path), index_file_list))
    return indexes(index_list)


def indexes_by_hash(index_list):
    standard_type_assertion.assert_list_pred('index_list', index_list, file_tree_snapshot.assert_index)
    table = {}

    hashes = []
    for index_main in index_list:
        hashes_main = set()
        for _, fileInfo in index_main.getPairList():
            hashes_main.add(fileInfo.getHash())
        hashes.append(hashes_main)

    hashes_all = set()
    for hashes_main in hashes:
        hashes_all |= hashes_main

    for hash_ in hashes_all:
        table[hash_] = [False] * len(index_list)

    for hash_ in table.keys():
        for index_index in range(len(index_list)):
            if hash_ in hashes[index_index]:
                table[hash_][index_index] = True

    return table


def get_data_hashes(data, keep_none=False):
    standard_type_assertion.assert_list('data', data)
    return list(map(lambda x: x.getHash() if x is not None else None, filter(lambda x: keep_none or x is not None, data)))


def get_same_hash(data):
    standard_type_assertion.assert_list('data', data)

    hashes = get_data_hashes(data)
    return hashes[0] if ibds_utils.is_same_list(hashes) else None
