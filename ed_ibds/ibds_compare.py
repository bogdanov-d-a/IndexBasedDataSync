from . import standard_type_assertion
from . import file_tree_snapshot
from . import ibds_utils
from . import ibds_tablegen


def multi_indexes(index_list, label_list, complete_locations, name=None):
    standard_type_assertion.assert_list_pred('index_list', index_list, file_tree_snapshot.assert_index)
    standard_type_assertion.assert_list_pred('label_list', label_list, standard_type_assertion.assert_string)
    standard_type_assertion.assert_set_pred('complete_locations', complete_locations, standard_type_assertion.assert_integer)

    table = ibds_tablegen.indexes(index_list)
    complete_locations_list = sorted(list(complete_locations))

    diff_data = []
    incomplete_location = []

    for path, data in ibds_utils.key_sorted_dict_items(table):
        if (ibds_tablegen.get_same_hash(data) is None):
            diff_data.append(path)

        incomplete_count = 0
        for complete_location_index in complete_locations_list:
            if data[complete_location_index] is None:
                incomplete_count += 1

        if incomplete_count != 0:
            incomplete_location.append(path)

    print_lists = [('Different data:', diff_data), ('Missing from complete location:', incomplete_location)]
    ibds_utils.print_lists(print_lists, name)


def multi_index_files(index_file_list, label_list, complete_locations, name=None):
    standard_type_assertion.assert_list_pred('index_file_list', index_file_list, standard_type_assertion.assert_string)
    standard_type_assertion.assert_list_pred('label_list', label_list, standard_type_assertion.assert_string)
    standard_type_assertion.assert_set_pred('complete_locations', complete_locations, standard_type_assertion.assert_integer)

    index_list = list(map(lambda index_file: file_tree_snapshot.load_index(index_file), index_file_list))
    multi_indexes(index_list, label_list, complete_locations, name)


def multi_indexes_by_hash(index_list, label_list, name=None):
    standard_type_assertion.assert_list_pred('index_list', index_list, file_tree_snapshot.assert_index)
    standard_type_assertion.assert_list_pred('label_list', label_list, standard_type_assertion.assert_string)

    table = ibds_tablegen.indexes_by_hash(index_list)

    unique_data = []

    for hash_, data in ibds_utils.key_sorted_dict_items(table):
        true_count = data.count(True)
        if true_count == 0:
            raise Exception('multi_indexes_by_hash true_count == 0')
        elif true_count == 1:
            unique_data.append(hash_)

    print_lists = [('Unique data:', unique_data)]
    ibds_utils.print_lists(print_lists, name)


def multi_index_by_hash_files(index_file_list, label_list, name=None):
    standard_type_assertion.assert_list_pred('index_file_list', index_file_list, standard_type_assertion.assert_string)
    standard_type_assertion.assert_list_pred('label_list', label_list, standard_type_assertion.assert_string)

    index_list = list(map(lambda index_file: file_tree_snapshot.load_index(index_file), index_file_list))
    multi_indexes_by_hash(index_list, label_list, name)
