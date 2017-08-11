import ibds_tablegen
import collection_data


def multi(collection_name, storage_devices):
    paths = []

    for storage_device in storage_devices:
        paths.append(collection_data.gen_index_file_path(collection_name, storage_device))

    return ibds_tablegen.index_files(paths)
