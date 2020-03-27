import ed_ibds.ibds_tablegen
import ed_ibds.path_generator


def multi(data_dir, collection_name, storage_devices):
    paths = []

    for storage_device in storage_devices:
        paths.append(ed_ibds.path_generator.gen_index_file_path(collection_name, storage_device, data_dir))

    return ed_ibds.ibds_tablegen.index_files(paths)
