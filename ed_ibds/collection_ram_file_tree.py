import ed_ibds.ram_file_tree
import ed_ibds.collection_data
import ed_ibds.file_tree_snapshot


# TODO: load common data there
def get_tree(data_dir, collection_dict, collection):
    data = ed_ibds.ram_file_tree.Directory('')

    for location in collection_dict[collection][0]:
        index = ed_ibds.file_tree_snapshot.load_index(ed_ibds.collection_data.gen_index_file_path(collection, location.getStorageDevice(), data_dir))
        for path, data_ in index.getPairList():
            data.add_file_path(path.split(ed_ibds.file_tree_snapshot.INDEX_PATH_SEPARATOR))

    return data


def explore(data_dir, collection_dict, collection):
    ed_ibds.ram_file_tree.explore(get_tree(data_dir, collection_dict, collection))
