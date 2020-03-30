import ed_ibds.standard_type_assertion


def _str_from_suffix(obj):
    if type(obj) is str:
        return obj
    elif type(obj) is ed_ibds.storage_device.StorageDevice:
        return obj.getName()
    else:
        raise Exception('unknown object type')


def gen_index_file_path(collection, suffix, data_dir):
    ed_ibds.standard_type_assertion.assert_string('collection', collection)

    prefix = data_dir + '\\' if data_dir is not None else ''
    return prefix + collection + '-' + _str_from_suffix(suffix) + '.txt'


def gen_common_file_path(collection, data_dir):
    return gen_index_file_path(collection, 'Common', data_dir)


def gen_hashset_file_path(collection, data_dir):
    return gen_index_file_path(collection, 'Hashset', data_dir)
