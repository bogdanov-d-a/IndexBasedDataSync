import os
from . import ibds_utils
from . import path_generator
from . import standard_type_assertion


def generate_target_file_list(collection_dict):
    standard_type_assertion.assert_dict('collection_dict', collection_dict)
    list_ = []

    for name, data in collection_dict.items():
        for location in data[0]:
            list_.append(path_generator.gen_index_file_path(name, location.getStorageDevice(), None))
        list_.append(path_generator.gen_common_file_path(name, None))
        list_.append(path_generator.gen_hashset_file_path(name, None))

    return list_


def generate_actual_file_list(data_dir):
    standard_type_assertion.assert_string('data_dir', data_dir)
    return os.listdir(data_dir)


def check_data_file_set(data_dir, collection_dict):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_dict('collection_dict', collection_dict)

    target = set(generate_target_file_list(collection_dict))
    actual = set(generate_actual_file_list(data_dir))
    ibds_utils.print_lists([['Odd', actual - target], ['Missing', target - actual]])
