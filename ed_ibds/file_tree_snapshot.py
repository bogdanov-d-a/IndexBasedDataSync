import os
import codecs
from edpu import file_hashing
from . import standard_type_assertion
from . import file_tree_scanner
from . import ibds_utils


INDEX_PATH_SEPARATOR = '\\'


def assert_file_info(name, data):
    if type(data) is not FileInfo:
        raise TypeError(name + ' should be FileInfo')


def assert_index(name, data):
    if type(data) is not Index:
        raise TypeError(name + ' should be index')


class FileInfo:
    def __init__(self, mtime, hash_):
        self.setMtime(mtime)
        self.setHash(hash_)

    def getMtime(self):
        return self._mtime

    def setMtime(self, mtime):
        standard_type_assertion.assert_float('mtime', mtime)
        self._mtime = mtime

    def getHash(self):
        return self._hash

    def setHash(self, hash_):
        standard_type_assertion.assert_string('hash', hash_)
        self._hash = hash_


class Index:
    def __init__(self):
        self._data = {}

    def addData(self, path, fileInfo):
        standard_type_assertion.assert_string('path', path)
        assert_file_info('fileInfo', fileInfo)
        self._data[path] = fileInfo

    def hasData(self, path):
        standard_type_assertion.assert_string('path', path)
        return path in self._data

    def getData(self, path):
        standard_type_assertion.assert_string('path', path)
        return self._data[path]

    def getPairList(self):
        return ibds_utils.key_sorted_dict_items(self._data)

    def getKeySet(self):
        return set(self._data.keys())


def create_index(tree_path, skip_paths):
    standard_type_assertion.assert_string('tree_path', tree_path)
    standard_type_assertion.assert_list_pred('skip_paths', skip_paths, standard_type_assertion.assert_string)

    index = Index()

    for rel_path in file_tree_scanner.scan(tree_path, skip_paths):
        rel_path_key = INDEX_PATH_SEPARATOR.join(rel_path)
        abs_path = os.path.join(tree_path, os.sep.join(rel_path))
        print('Calculating hash for ' + rel_path_key)
        index.addData(INDEX_PATH_SEPARATOR.join(rel_path), FileInfo(os.path.getmtime(abs_path), file_hashing.sha1_file(abs_path)))

    return index


def update_index(old_index, tree_path, skip_paths, skip_mtime):
    assert_index('old_index', old_index)
    standard_type_assertion.assert_string('tree_path', tree_path)
    standard_type_assertion.assert_list_pred('skip_paths', skip_paths, standard_type_assertion.assert_string)
    standard_type_assertion.assert_bool('skip_mtime', skip_mtime)

    index = Index()

    for rel_path in file_tree_scanner.scan(tree_path, skip_paths):
        abs_path = os.path.join(tree_path, os.sep.join(rel_path))

        if not skip_mtime:
            mdate = os.path.getmtime(abs_path)

        rel_path_key = INDEX_PATH_SEPARATOR.join(rel_path)

        if old_index.hasData(rel_path_key) and (skip_mtime or old_index.getData(rel_path_key).getMtime() == mdate):
            hash_ = old_index.getData(rel_path_key).getHash()
            if skip_mtime:
                mdate = old_index.getData(rel_path_key).getMtime()
        else:
            print('Calculating hash for ' + rel_path_key)
            hash_ = file_hashing.sha1_file(abs_path)
            if skip_mtime:
                mdate = os.path.getmtime(abs_path)

        index.addData(rel_path_key, FileInfo(mdate, hash_))

    return index


def load_index(file_path):
    standard_type_assertion.assert_string('file_path', file_path)

    with codecs.open(file_path, 'r', 'utf-8-sig') as input_:
        data_ = Index()

        for line in input_.readlines():
            if line[-1] == '\n':
                line = line[:-1]
            parts = line.split(' ', 2)
            if len(parts) != 3:
                raise Exception('load_index bad format')
            data_.addData(parts[2], FileInfo(float(parts[0]), parts[1]))

        return data_


def save_index(index, file_path):
    assert_index('index', index)
    standard_type_assertion.assert_string('file_path', file_path)

    with codecs.open(file_path, 'w', 'utf-8-sig') as output:
        for path, data in index.getPairList():
            output.write(str(data.getMtime()))
            output.write(' ')
            output.write(data.getHash())
            output.write(' ')
            output.write(path)
            output.write('\n')


def update_index_file(tree_path, index_path, skip_paths, skip_mtime):
    standard_type_assertion.assert_string('tree_path', tree_path)
    standard_type_assertion.assert_string('index_path', index_path)
    standard_type_assertion.assert_list_pred('skip_paths', skip_paths, standard_type_assertion.assert_string)
    standard_type_assertion.assert_bool('skip_mtime', skip_mtime)

    if os.path.isfile(index_path):
        old_index = load_index(index_path)
        new_index = update_index(old_index, tree_path, skip_paths, skip_mtime)
    else:
        new_index = create_index(tree_path, skip_paths)
    save_index(new_index, index_path)
