import ed_ibds.ibds_tablegen
import ed_ibds.path_generator


def multi(data_dir, collection_name, storage_devices):
    ed_ibds.standard_type_assertion.assert_string('data_dir', data_dir)
    ed_ibds.standard_type_assertion.assert_string('collection_name', collection_name)
    ed_ibds.standard_type_assertion.assert_list_pred('storage_devices', storage_devices, ed_ibds.storage_device.assert_storage_device)

    paths = list(map(lambda storage_device: ed_ibds.path_generator.gen_index_file_path(collection_name, storage_device, data_dir), storage_devices))
    return ed_ibds.ibds_tablegen.index_files(paths)
