import ed_ibds


def collection_common(data_dir, collection_name, skip_paths):
    ed_ibds.standard_type_assertion.assert_string('data_dir', data_dir)
    ed_ibds.standard_type_assertion.assert_string('collection_name', collection_name)
    ed_ibds.standard_type_assertion.assert_list('skip_paths', skip_paths)

    data = ed_ibds.collection_definition.load_common_data(ed_ibds.path_generator.gen_common_file_path(collection_name, data_dir))
    table = {}

    for path, hash_ in data:
        if ed_ibds.ibds_utils.path_needs_skip(path.split(ed_ibds.file_tree_snapshot.INDEX_PATH_SEPARATOR), skip_paths):
            continue
        if hash_ not in table:
            table[hash_] = []
        table[hash_].append(path)

    for hash_, paths in ed_ibds.ibds_utils.key_sorted_dict_items(table):
        if (len(paths) > 1):
            print(hash_ + ' ' + str(paths))


def collection_storage_device(data_dir, collection_name, storage_device):
    ed_ibds.standard_type_assertion.assert_string('data_dir', data_dir)
    ed_ibds.standard_type_assertion.assert_string('collection_name', collection_name)
    ed_ibds.storage_device.assert_storage_device('storage_device', storage_device)

    data = ed_ibds.file_tree_snapshot.load_index(ed_ibds.path_generator.gen_index_file_path(collection_name, storage_device, data_dir))
    table = {}

    for path, info in data.getPairList():
        if info.getHash() not in table:
            table[info.getHash()] = []
        table[info.getHash()].append(path)

    for _, paths in ed_ibds.ibds_utils.key_sorted_dict_items(table):
        if (len(paths) > 1):
            print(paths)


def collections_common(data_dir, collection_dict):
    ed_ibds.standard_type_assertion.assert_string('data_dir', data_dir)
    ed_ibds.standard_type_assertion.assert_dict('collection_dict', collection_dict)

    for collection_name, data in ed_ibds.ibds_utils.key_sorted_dict_items(collection_dict):
        collection_common(data_dir, collection_name, data[2])
