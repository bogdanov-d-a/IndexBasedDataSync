import os
import edpu.user_interaction
import ed_ibds.standard_type_assertion
import ed_ibds.ibds_utils
import ed_ibds.storage_device


def locations_to_storage_devices(locations):
    return list(map(lambda x: x.getStorageDevice(), locations))


def _str_from_suffix(obj):
    if type(obj) is str:
        return obj
    elif type(obj) is ed_ibds.storage_device.StorageDevice:
        return obj.getName()
    else:
        raise Exception('unknown object type')


def gen_index_file_path(collection, suffix, data_dir):
    ed_ibds.standard_type_assertion.assert_string('collection', collection)

    prefix = ''
    if data_dir is not None:
        prefix = data_dir + '\\'

    return prefix + collection + '-' + _str_from_suffix(suffix) + '.txt'


def gen_common_file_path(collection, data_dir):
    return gen_index_file_path(collection, 'Common', data_dir)


def gen_hashset_file_path(collection, data_dir):
    return gen_index_file_path(collection, 'Hashset', data_dir)


def pick_storage_device(device_list):
    list_ = []
    for device in device_list:
        list_.append(device.getName())
    return device_list[edpu.user_interaction.pick_option('Choose storage device', list_)]


def generate_target_file_list(collection_dict):
    list_ = []

    for name, data in collection_dict.items():
        for location in data[0]:
            list_.append(gen_index_file_path(name, location.getStorageDevice(), None))
        list_.append(gen_common_file_path(name, None))
        list_.append(gen_hashset_file_path(name, None))

    return list_


def generate_actual_file_list(data_dir):
    return os.listdir(data_dir)


def check_data_file_set(data_dir, collection_dict):
    target = set(generate_target_file_list(collection_dict))
    actual = set(generate_actual_file_list(data_dir))
    ed_ibds.ibds_utils.print_lists([['Odd', actual - target], ['Missing', target - actual]])
