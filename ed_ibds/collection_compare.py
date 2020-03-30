import ed_ibds.ibds_utils
import ed_ibds.path_generator
import ed_ibds.ibds_compare
import ed_ibds.standard_type_assertion
import ed_ibds.storage_device


def multi_storage_devices_of_collection(data_dir, collection_name, storage_devices, complete_storage_device_indices):
    ed_ibds.standard_type_assertion.assert_string('data_dir', data_dir)
    ed_ibds.standard_type_assertion.assert_string('collection_name', collection_name)
    ed_ibds.standard_type_assertion.assert_list_pred('storage_devices', storage_devices, ed_ibds.storage_device.assert_storage_device)
    ed_ibds.standard_type_assertion.assert_set_pred('complete_storage_device_indices', complete_storage_device_indices, ed_ibds.standard_type_assertion.assert_integer)

    paths = list(map(lambda storage_device: ed_ibds.path_generator.gen_index_file_path(collection_name, storage_device, data_dir), storage_devices))
    labels = list(map(lambda storage_device: storage_device.getName(), storage_devices))
    ed_ibds.ibds_compare.multi_index_files(paths, labels, complete_storage_device_indices, collection_name)


def collection(data_dir, collection_dict, collection_name):
    ed_ibds.standard_type_assertion.assert_string('data_dir', data_dir)
    ed_ibds.standard_type_assertion.assert_dict('collection_dict', collection_dict)
    ed_ibds.standard_type_assertion.assert_string('collection_name', collection_name)

    locations = collection_dict[collection_name][0]
    complete_location_indices = { index for _, index in filter(lambda elem: elem[0].isComplete(), zip(locations, range(len(locations)))) }
    multi_storage_devices_of_collection(data_dir, collection_name, ed_ibds.ibds_utils.locations_to_storage_devices(locations), complete_location_indices)


def collections(data_dir, collection_dict):
    ed_ibds.standard_type_assertion.assert_string('data_dir', data_dir)
    ed_ibds.standard_type_assertion.assert_dict('collection_dict', collection_dict)

    for collection_name, _ in ed_ibds.ibds_utils.key_sorted_dict_items(collection_dict):
        collection(data_dir, collection_dict, collection_name)
