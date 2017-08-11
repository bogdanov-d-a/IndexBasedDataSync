import codecs
import standard_type_assertion
import ibds_utils
import collection_data
import collection_tablegen
import ibds_tablegen


def save_common_data(common_data, file_path):
    output = codecs.open(file_path, 'w', 'utf-8-sig')
    for path, hash_ in common_data:
        output.write(hash_)
        output.write(' ')
        output.write(path)
        output.write('\n')
    output.close()


def load_common_data(file_path):
    standard_type_assertion.assert_string('file_path', file_path)

    input_ = codecs.open(file_path, 'r', 'utf-8-sig')
    data_ = []

    for line in input_.readlines():
        if line[-1] == '\n':
            line = line[:-1]
        parts = line.split(' ', 1)
        if len(parts) != 2:
            raise Exception('load_common_data bad format')
        data_.append((parts[1], parts[0]))

    input_.close()
    return data_


def save_hashset_data(hashset_data, file_path):
    output = codecs.open(file_path, 'w', 'utf-8-sig')
    for hash_ in sorted(list(hashset_data)):
        output.write(hash_)
        output.write('\n')
    output.close()


def generate_collection_definition(collection_name):
    locations = collection_data.COLLECTION_MAP[collection_name]

    common_data = []
    table = collection_tablegen.multi(collection_name, collection_data.locations_to_storage_devices(locations))
    for path, data in ibds_utils.key_sorted_dict_items(table):
        for hash_ in sorted(list(set(ibds_tablegen.get_data_hashes(data)))):
            common_data.append((path, hash_))
    save_common_data(common_data, collection_data.gen_common_file_path(collection_name))

    hashset = set([])
    for path, hash_ in common_data:
        hashset.add(hash_)
    save_hashset_data(hashset, collection_data.gen_hashset_file_path(collection_name))


def generate_collections_definition():
    for collection_name, locations in ibds_utils.key_sorted_dict_items(collection_data.COLLECTION_MAP):
        generate_collection_definition(collection_name)
