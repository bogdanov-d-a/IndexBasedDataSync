from . import standard_type_assertion
from . import collection_definition
from . import ibds_utils
from . import file_tree_snapshot
from . import path_generator
from . import storage_device


def _collection_common(data_dir, collection_name, skip_paths):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_string('collection_name', collection_name)
    standard_type_assertion.assert_list('skip_paths', skip_paths)

    data = collection_definition.load_common_data(path_generator.gen_common_file_path(collection_name, data_dir))
    table = {}

    for path, hash_ in data:
        if ibds_utils.path_needs_skip(path.split(file_tree_snapshot.INDEX_PATH_SEPARATOR), skip_paths):
            continue
        if hash_ not in table:
            table[hash_] = []
        table[hash_].append(path)

    for hash_, paths in ibds_utils.key_sorted_dict_items(table):
        if (len(paths) > 1):
            print(hash_ + ' ' + str(paths))


def _collection_storage_device(data_dir, collection_name, storage_device_):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_string('collection_name', collection_name)
    storage_device.assert_storage_device('storage_device_', storage_device_)

    data = file_tree_snapshot.load_index(path_generator.gen_index_file_path(collection_name, storage_device_, data_dir))
    table = {}

    for path, info in data.getPairList():
        if info.getHash() not in table:
            table[info.getHash()] = []
        table[info.getHash()].append(path)

    for _, paths in ibds_utils.key_sorted_dict_items(table):
        if (len(paths) > 1):
            print(paths)


def collections_common(data_dir, collection_dict):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_dict('collection_dict', collection_dict)

    for collection_name, data in ibds_utils.key_sorted_dict_items(collection_dict):
        _collection_common(data_dir, collection_name, data[2])
