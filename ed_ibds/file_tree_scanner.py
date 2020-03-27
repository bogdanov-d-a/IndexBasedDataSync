import os
import ed_ibds.standard_type_assertion
import ed_ibds.ibds_utils


EXCLUDE_FILE_NAMES_DEFAULT = ['desktop.ini', 'Thumbs.db', '.hidden', '.nomedia', '.camera', 'sync.ffs_db']


def scan(root_path, skip_paths, exclude_file_names=EXCLUDE_FILE_NAMES_DEFAULT):
    ed_ibds.standard_type_assertion.assert_string('root_path', root_path)
    ed_ibds.standard_type_assertion.assert_list('exclude_file_names', exclude_file_names, ed_ibds.standard_type_assertion.assert_string)

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
            if cur_file not in exclude_file_names and not ed_ibds.ibds_utils.path_needs_skip(rel_path + [cur_file], skip_paths):
                file_tree.append(rel_path + [cur_file])

    return file_tree
