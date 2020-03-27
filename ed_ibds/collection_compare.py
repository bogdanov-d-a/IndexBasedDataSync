import ed_ibds.ibds_utils
import ed_ibds.path_generator
import ed_ibds.ibds_compare


def multi_storage_devices_of_collection(data_dir, collection_name, storage_devices, complete_storage_device_indices):
    paths = []
    labels = []

    for storage_device in storage_devices:
        paths.append(ed_ibds.path_generator.gen_index_file_path(collection_name, storage_device, data_dir))
        labels.append(storage_device.getName())

    ed_ibds.ibds_compare.multi_index_files(paths, labels, complete_storage_device_indices, collection_name)


def collection(data_dir, collection_dict, collection_name):
    locations = collection_dict[collection_name][0]

    complete_location_indices = set([])
    index = 0
    for location in locations:
        if location.isComplete():
            complete_location_indices.add(index)
        index += 1

    multi_storage_devices_of_collection(data_dir, collection_name, ed_ibds.ibds_utils.locations_to_storage_devices(locations), complete_location_indices)


def collections(data_dir, collection_dict):
    for collection_name, _ in ed_ibds.ibds_utils.key_sorted_dict_items(collection_dict):
        collection(data_dir, collection_dict, collection_name)
