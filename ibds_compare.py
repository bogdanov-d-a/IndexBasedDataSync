import standard_type_assertion
import file_tree_snapshot
import ibds_utils
import ibds_tablegen


def multi_indexes(index_list, label_list, complete_locations, name=None):
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
    index_list = []
    for index_file in index_file_list:
        index_list.append(file_tree_snapshot.load_index(index_file))

    multi_indexes(index_list, label_list, complete_locations, name)
