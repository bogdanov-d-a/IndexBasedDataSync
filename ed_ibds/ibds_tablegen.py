import ed_ibds.standard_type_assertion
import ed_ibds.file_tree_snapshot
import ed_ibds.ibds_utils


def indexes(index_list):
    ed_ibds.standard_type_assertion.assert_list('index_list', index_list, ed_ibds.file_tree_snapshot.assert_index)

    table = {}

    paths = set()
    for index_main in index_list:
        paths = paths | index_main.getKeySet()

    none_list = []
    for _ in range(len(index_list)):
        none_list.append(None)

    for path in paths:
        table[path] = none_list[:]

    for path in table.keys():
        for index_index in range(len(index_list)):
            if index_list[index_index].hasData(path):
                table[path][index_index] = index_list[index_index].getData(path)

    return table


def index_files(index_file_list):
    index_list = []
    for path in index_file_list:
        index_list.append(ed_ibds.file_tree_snapshot.load_index(path))

    return indexes(index_list)


def get_data_hashes(data):
    return list(map(lambda x: x.getHash(), filter(lambda x: x is not None, data)))


def get_same_hash(data):
    hashes = get_data_hashes(data)

    if ed_ibds.ibds_utils.is_same_list(hashes):
        return hashes[0]
    else:
        return None
