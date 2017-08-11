import os
import standard_type_assertion


EXCLUDE_FILE_NAMES_DEFAULT = ['desktop.ini', 'Thumbs.db', '.hidden', '.nomedia', '.camera']


def scan(root_path, exclude_file_names=EXCLUDE_FILE_NAMES_DEFAULT):
    standard_type_assertion.assert_string('root_path', root_path)
    standard_type_assertion.assert_list('exclude_file_names', exclude_file_names, standard_type_assertion.assert_string)

    if not os.path.isdir(root_path):
        raise Exception(root_path + ' does not exist')

    file_tree = []

    for cur_root_path, dirs, files in os.walk(root_path):
        rel_path_text = os.path.relpath(cur_root_path, root_path)
        if rel_path_text == '.':
            rel_path = []
        else:
            rel_path = rel_path_text.split(os.sep)

        for cur_file in files:
            if cur_file not in exclude_file_names:
                file_tree.append(rel_path + [cur_file])

    return file_tree
