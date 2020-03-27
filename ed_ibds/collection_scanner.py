import edpu.storage_finder
import ed_ibds.path_generator
import ed_ibds.ibds_utils
import ed_ibds.standard_type_assertion
import ed_ibds.file_tree_snapshot
import ed_ibds.storage_device


def _scan_collection_storage_device(data_dir, collection_name, storage_device, data_path, skip_paths):
    ed_ibds.standard_type_assertion.assert_string('collection_name', collection_name)
    ed_ibds.storage_device.assert_storage_device('storage_device', storage_device)
    ed_ibds.standard_type_assertion.assert_string('data_path', data_path)

    ed_ibds.file_tree_snapshot.update_index_file(data_path, ed_ibds.path_generator.gen_index_file_path(collection_name, storage_device, data_dir), skip_paths)


def scan_storage_device(data_dir, collection_dict, storage_device):
    ed_ibds.storage_device.assert_storage_device('storage_device', storage_device)

    path_prefix = ''
    if storage_device.isRemovable():
        path_prefix = edpu.storage_finder.keep_getting_storage_path(storage_device.getName())

    for collection_name, data in ed_ibds.ibds_utils.key_sorted_dict_items(collection_dict):
        for location in data[0]:
            if location.getStorageDevice().getName() == storage_device.getName():
                _scan_collection_storage_device(data_dir, collection_name, storage_device, path_prefix + location.getPath(), data[1])
