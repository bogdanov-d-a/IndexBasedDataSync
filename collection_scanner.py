import collection_data
import ibds_utils
import standard_type_assertion
import file_tree_snapshot
import edpu.storage_finder


def _scan_collection_storage_device(collection_name, storage_device, data_path, skip_paths):
    standard_type_assertion.assert_string('collection_name', collection_name)
    collection_data.assert_storage_device('storage_device', storage_device)
    standard_type_assertion.assert_string('data_path', data_path)

    file_tree_snapshot.update_index_file(data_path, collection_data.gen_index_file_path(collection_name, storage_device), skip_paths)


def scan_storage_device(storage_device):
    collection_data.assert_storage_device('storage_device', storage_device)

    path_prefix = ''
    if storage_device.isRemovable():
        path_prefix = edpu.storage_finder.keep_getting_storage_path(storage_device.getName())

    for collection_name, data in ibds_utils.key_sorted_dict_items(collection_data.COLLECTION_MAP):
        for location in data[0]:
            if location.getStorageDevice().getName() == storage_device.getName():
                _scan_collection_storage_device(collection_name, storage_device, path_prefix + location.getPath(), data[1])
