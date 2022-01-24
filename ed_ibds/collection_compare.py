from . import ibds_utils
from . import path_generator
from . import ibds_compare
from . import standard_type_assertion
from . import storage_device


def multi_storage_devices_of_collection(data_dir, collection_name, storage_devices, complete_storage_device_indices):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_string('collection_name', collection_name)
    standard_type_assertion.assert_list_pred('storage_devices', storage_devices, storage_device.assert_storage_device)
    standard_type_assertion.assert_set_pred('complete_storage_device_indices', complete_storage_device_indices, standard_type_assertion.assert_integer)

    paths = list(map(lambda storage_device_: path_generator.gen_index_file_path(collection_name, storage_device_, data_dir), storage_devices))
    ibds_compare.multi_index_files(paths, complete_storage_device_indices, collection_name)


def multi_storage_devices_of_collection_by_hash(data_dir, collection_name, storage_devices):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_string('collection_name', collection_name)
    standard_type_assertion.assert_list_pred('storage_devices', storage_devices, storage_device.assert_storage_device)

    paths = list(map(lambda storage_device_: path_generator.gen_index_file_path(collection_name, storage_device_, data_dir), storage_devices))
    ibds_compare.multi_index_by_hash_files(paths, collection_name)


def collection(data_dir, collection_dict, collection_name):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_dict('collection_dict', collection_dict)
    standard_type_assertion.assert_string('collection_name', collection_name)

    locations = collection_dict[collection_name][0]
    complete_location_indices = { index for _, index in filter(lambda elem: elem[0].isComplete(), zip(locations, range(len(locations)))) }
    multi_storage_devices_of_collection(data_dir, collection_name, ibds_utils.locations_to_storage_devices(locations), complete_location_indices)


def collection_by_hash(data_dir, collection_dict, collection_name):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_dict('collection_dict', collection_dict)
    standard_type_assertion.assert_string('collection_name', collection_name)

    locations = collection_dict[collection_name][0]
    multi_storage_devices_of_collection_by_hash(data_dir, collection_name, ibds_utils.locations_to_storage_devices(locations))


def collections(data_dir, collection_dict):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_dict('collection_dict', collection_dict)

    for collection_name, _ in ibds_utils.key_sorted_dict_items(collection_dict):
        collection(data_dir, collection_dict, collection_name)


def collections_by_hash(data_dir, collection_dict):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_dict('collection_dict', collection_dict)

    for collection_name, _ in ibds_utils.key_sorted_dict_items(collection_dict):
        collection_by_hash(data_dir, collection_dict, collection_name)
