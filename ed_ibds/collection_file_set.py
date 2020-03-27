import os
import ed_ibds.ibds_utils
import ed_ibds.path_generator


def generate_target_file_list(collection_dict):
    list_ = []

    for name, data in collection_dict.items():
        for location in data[0]:
            list_.append(ed_ibds.path_generator.gen_index_file_path(name, location.getStorageDevice(), None))
        list_.append(ed_ibds.path_generator.gen_common_file_path(name, None))
        list_.append(ed_ibds.path_generator.gen_hashset_file_path(name, None))

    return list_


def generate_actual_file_list(data_dir):
    return os.listdir(data_dir)


def check_data_file_set(data_dir, collection_dict):
    target = set(generate_target_file_list(collection_dict))
    actual = set(generate_actual_file_list(data_dir))
    ed_ibds.ibds_utils.print_lists([['Odd', actual - target], ['Missing', target - actual]])
