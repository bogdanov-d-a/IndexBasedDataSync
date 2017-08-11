import collection_data
import ibds_utils
import standard_type_assertion
import file_tree_snapshot
import user_path_manager


def _scan_collection_storage_device(collection_name, storage_device, data_path):
    standard_type_assertion.assert_string('collection_name', collection_name)
    collection_data.assert_storage_device('storage_device', storage_device)
    standard_type_assertion.assert_string('data_path', data_path)

    file_tree_snapshot.update_index_file(data_path, collection_data.gen_index_file_path(collection_name, storage_device))


def scan_storage_device(storage_device):
    collection_data.assert_storage_device('storage_device', storage_device)

    path_prefix = ''
    if storage_device.isRemovable():
        path_prefix = user_path_manager.keep_getting_device_path(storage_device.getName())

    for collection_name, locations in ibds_utils.key_sorted_dict_items(collection_data.COLLECTION_MAP):
        for location in locations:
            if location.getStorageDevice().getName() == storage_device.getName():
                _scan_collection_storage_device(collection_name, storage_device, path_prefix + location.getPath())
