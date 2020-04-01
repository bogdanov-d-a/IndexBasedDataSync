from . import standard_type_assertion
from . import ibds_tablegen
from . import path_generator
from . import storage_device


def multi(data_dir, collection_name, storage_devices):
    standard_type_assertion.assert_string('data_dir', data_dir)
    standard_type_assertion.assert_string('collection_name', collection_name)
    standard_type_assertion.assert_list_pred('storage_devices', storage_devices, storage_device.assert_storage_device)

    paths = list(map(lambda storage_device_: path_generator.gen_index_file_path(collection_name, storage_device_, data_dir), storage_devices))
    return ibds_tablegen.index_files(paths)
