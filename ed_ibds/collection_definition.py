import codecs
from . import standard_type_assertion
from . import ibds_utils
from . import collection_tablegen
from . import ibds_tablegen
from . import path_generator


def save_common_data(common_data, file_path):
    standard_type_assertion.assert_list('common_data', common_data)
    standard_type_assertion.assert_string('file_path', file_path)

    with codecs.open(file_path, 'w', 'utf-8-sig') as output:
        for path, hash_ in common_data:
            output.write(hash_)
            output.write(' ')
            output.write(path)
            output.write('\n')


def load_common_data(file_path):
    standard_type_assertion.assert_string('file_path', file_path)

    with codecs.open(file_path, 'r', 'utf-8-sig') as input_:
        data_ = []

        for line in input_.readlines():
            if line[-1] == '\n':
                line = line[:-1]
            parts = line.split(' ', 1)
            if len(parts) != 2:
                raise Exception('load_common_data bad format')
            data_.append((parts[1], parts[0]))

        return data_


def save_hashset_data(hashset_data, file_path):
    standard_type_assertion.assert_set('hashset_data', hashset_data)
    standard_type_assertion.assert_string('file_path', file_path)

    with codecs.open(file_path, 'w', 'utf-8-sig') as output:
        for hash_ in sorted(list(hashset_data)):
            output.write(hash_)
            output.write('\n')


def _generate_collection_definition(data_dir, collection_dict, collection_name):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_dict('collection_dict', collection_dict)
    standard_type_assertion.assert_string('collection_name', collection_name)

    locations = collection_dict[collection_name][0]

    common_data = []
    table = collection_tablegen.multi(data_dir, collection_name, ibds_utils.locations_to_storage_devices(locations))
    for path, data in ibds_utils.key_sorted_dict_items(table):
        for hash_ in sorted(list(set(ibds_tablegen.get_data_hashes(data)))):
            common_data.append((path, hash_))
    save_common_data(common_data, path_generator.gen_common_file_path(collection_name, data_dir))

    hashset = { hash_ for _, hash_ in common_data }
    save_hashset_data(hashset, path_generator.gen_hashset_file_path(collection_name, data_dir))


def generate_collections_definition(data_dir, collection_dict):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_dict('collection_dict', collection_dict)

    for collection_name, _ in ibds_utils.key_sorted_dict_items(collection_dict):
        _generate_collection_definition(data_dir, collection_dict, collection_name)
