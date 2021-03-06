import os
from . import standard_type_assertion
from . import ibds_utils


def scan(root_path, skip_paths):
    standard_type_assertion.assert_string('root_path', root_path)
    standard_type_assertion.assert_list_pred('skip_paths', skip_paths, standard_type_assertion.assert_string)

    if not os.path.isdir(root_path):
        raise Exception(root_path + ' does not exist')

    file_tree = []

    for cur_root_path, _, files in os.walk(root_path):
        rel_path_text = os.path.relpath(cur_root_path, root_path)
        if rel_path_text == '.':
            rel_path = []
        else:
            rel_path = rel_path_text.split(os.sep)

        for cur_file in files:
            if not ibds_utils.path_needs_skip(rel_path + [cur_file], skip_paths):
                file_tree.append(rel_path + [cur_file])

    return file_tree
