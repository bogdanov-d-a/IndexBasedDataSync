import file_tree_snapshot
import ibds_utils
import collection_data
import collection_definition


def collection_common(collection, skip_paths):
    data = collection_definition.load_common_data(collection_data.gen_common_file_path(collection))
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


def collection_storage_device(collection, storage_device):
    data = file_tree_snapshot.load_index(collection_data.gen_index_file_path(collection, storage_device))
    table = {}

    for path, info in data.getPairList():
        if info.getHash() not in table:
            table[info.getHash()] = []
        table[info.getHash()].append(path)

    for hash_, paths in ibds_utils.key_sorted_dict_items(table):
        if (len(paths) > 1):
            print(paths)


def collections_common():
    for collection_name, data in ibds_utils.key_sorted_dict_items(collection_data.COLLECTION_MAP):
        collection_common(collection_name, data[2])
