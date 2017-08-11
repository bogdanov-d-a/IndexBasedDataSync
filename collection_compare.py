import ibds_utils
import collection_data
import ibds_compare


def multi_storage_devices_of_collection(collection_name, storage_devices, complete_storage_device_indices):
    paths = []
    labels = []

    for storage_device in storage_devices:
        paths.append(collection_data.gen_index_file_path(collection_name, storage_device))
        labels.append(storage_device.getName())

    ibds_compare.multi_index_files(paths, labels, complete_storage_device_indices, collection_name)


def collection(collection_name):
    locations = collection_data.COLLECTION_MAP[collection_name]

    complete_location_indices = set([])
    index = 0
    for location in locations:
        if location.isComplete():
            complete_location_indices.add(index)
        index += 1

    multi_storage_devices_of_collection(collection_name, collection_data.locations_to_storage_devices(locations), complete_location_indices)


def collections():
    for collection_name, locations in ibds_utils.key_sorted_dict_items(collection_data.COLLECTION_MAP):
        collection(collection_name)
