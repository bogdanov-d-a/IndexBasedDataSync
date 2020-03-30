import ed_ibds.standard_type_assertion
import ed_ibds.file_tree_snapshot
import ed_ibds.ibds_utils


def indexes(index_list):
    ed_ibds.standard_type_assertion.assert_list_pred('index_list', index_list, ed_ibds.file_tree_snapshot.assert_index)
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
    ed_ibds.standard_type_assertion.assert_list_pred('index_file_list', index_file_list, ed_ibds.standard_type_assertion.assert_string)

    index_list = list(map(lambda path: ed_ibds.file_tree_snapshot.load_index(path), index_file_list))
    return indexes(index_list)


def get_data_hashes(data):
    ed_ibds.standard_type_assertion.assert_list('data', data)
    return list(map(lambda x: x.getHash(), filter(lambda x: x is not None, data)))


def get_same_hash(data):
    ed_ibds.standard_type_assertion.assert_list('data', data)

    hashes = get_data_hashes(data)
    return hashes[0] if ed_ibds.ibds_utils.is_same_list(hashes) else None
