from . import standard_type_assertion
from . import storage_device
import os


def _gen_impl(data_dir, infixes):
    standard_type_assertion.assert_list_pred('infixes', infixes, standard_type_assertion.assert_string)

    prefix = data_dir + os.path.sep if data_dir is not None else ''
    return prefix + '-'.join(infixes) + '.txt'


def gen_index_file_path(collection, storage_device_, data_dir):
    standard_type_assertion.assert_string('collection', collection)
    storage_device.assert_storage_device('storage_device_', storage_device_)

    return _gen_impl(data_dir, [collection, storage_device_.getName()])


def gen_common_file_path(collection, data_dir):
    return _gen_impl(data_dir, [collection, 'Common'])


def gen_hashset_file_path(collection, data_dir):
    return _gen_impl(data_dir, [collection, 'Hashset'])
