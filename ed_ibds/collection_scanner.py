from edpu import storage_finder
from . import path_generator
from . import ibds_utils
from . import standard_type_assertion
from . import file_tree_snapshot
from . import storage_device


def _scan_collection_storage_device(data_dir, collection_name, storage_device_, data_path, skip_paths):
    standard_type_assertion.assert_string('collection_name', collection_name)
    storage_device.assert_storage_device('storage_device_', storage_device_)
    standard_type_assertion.assert_string('data_path', data_path)
    standard_type_assertion.assert_list_pred('skip_paths', skip_paths, standard_type_assertion.assert_string)

    file_tree_snapshot.update_index_file(data_path, path_generator.gen_index_file_path(collection_name, storage_device_, data_dir), skip_paths)


def scan_storage_device(data_dir, collection_dict, storage_device_):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_dict('collection_dict', collection_dict)
    storage_device.assert_storage_device('storage_device_', storage_device_)

    path_prefix = storage_finder.keep_getting_storage_path(storage_device_.getName()) if storage_device_.isRemovable() else ''

    for collection_name, data in ibds_utils.key_sorted_dict_items(collection_dict):
        for location in data[0]:
            if location.getStorageDevice().getName() == storage_device_.getName():
                _scan_collection_storage_device(data_dir, collection_name, storage_device_, path_prefix + location.getPath(), data[1])
