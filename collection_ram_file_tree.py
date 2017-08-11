import ram_file_tree
import collection_data
import file_tree_snapshot


# TODO: load common data there
def get_tree(collection):
    data = ram_file_tree.Directory('')

    for location in collection_data.COLLECTION_MAP[collection]:
        index = file_tree_snapshot.load_index(collection_data.gen_index_file_path(collection, location.getStorageDevice()))
        for path, data_ in index.getPairList():
            data.add_file_path(path.split(file_tree_snapshot.INDEX_PATH_SEPARATOR))

    return data


def explore(collection):
    ram_file_tree.explore(get_tree(collection))
