from . import ram_file_tree
from . import path_generator
from . import file_tree_snapshot


# TODO: load common data there
def get_tree(data_dir, collection_dict, collection):
    data = ram_file_tree.Directory('')

    for location in collection_dict[collection][0]:
        index = file_tree_snapshot.load_index(path_generator.gen_index_file_path(collection, location.getStorageDevice(), data_dir))
        for path, _ in index.getPairList():
            data.add_file_path(path.split(file_tree_snapshot.INDEX_PATH_SEPARATOR))

    return data


def explore(data_dir, collection_dict, collection):
    ram_file_tree.explore(get_tree(data_dir, collection_dict, collection))
