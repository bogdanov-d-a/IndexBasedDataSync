from edpu import file_tree_walker
from . import standard_type_assertion
from . import ibds_utils


def scan(root_path, skip_paths):
    standard_type_assertion.assert_string('root_path', root_path)
    standard_type_assertion.assert_list_pred('skip_paths', skip_paths, standard_type_assertion.assert_string)

    return file_tree_walker.walk(
        root_path,
        lambda type, path: type == file_tree_walker.TYPE_DIR or ibds_utils.path_needs_skip(path, skip_paths)
    ).get(file_tree_walker.TYPE_FILE)
