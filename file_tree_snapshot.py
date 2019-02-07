import os
import codecs
import file_tree_scanner
import standard_type_assertion
import hash_facade
import ibds_utils


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
        return set(self._data.keys());


def create_index(tree_path, skip_paths):
    standard_type_assertion.assert_string('tree_path', tree_path)

    index = Index()

    for rel_path in file_tree_scanner.scan(tree_path, skip_paths):
        rel_path_key = INDEX_PATH_SEPARATOR.join(rel_path)
        abs_path = os.path.join(tree_path, os.sep.join(rel_path))
        print('Calculating hash for ' + rel_path_key)
        index.addData(INDEX_PATH_SEPARATOR.join(rel_path), FileInfo(os.path.getmtime(abs_path), hash_facade.sha1(abs_path)))

    return index


def update_index(old_index, tree_path, skip_paths):
    assert_index('old_index', old_index)
    standard_type_assertion.assert_string('tree_path', tree_path)

    index = Index()

    for rel_path in file_tree_scanner.scan(tree_path, skip_paths):
        abs_path = os.path.join(tree_path, os.sep.join(rel_path))
        mdate = os.path.getmtime(abs_path)
        rel_path_key = INDEX_PATH_SEPARATOR.join(rel_path)

        if (old_index.hasData(rel_path_key)) and (old_index.getData(rel_path_key).getMtime() == mdate):
            hash_ = old_index.getData(rel_path_key).getHash()
        else:
            print('Calculating hash for ' + rel_path_key)
            hash_ = hash_facade.sha1(abs_path)
        index.addData(rel_path_key, FileInfo(mdate, hash_))

    return index


def load_index(file_path):
    standard_type_assertion.assert_string('file_path', file_path)

    input_ = codecs.open(file_path, 'r', 'utf-8-sig')
    data_ = Index()

    for line in input_.readlines():
        if line[-1] == '\n':
            line = line[:-1]
        parts = line.split(' ', 2)
        if len(parts) != 3:
            raise Exception('load_index bad format')
        data_.addData(parts[2], FileInfo(float(parts[0]), parts[1]))

    input_.close()
    return data_


def save_index(index, file_path):
    assert_index('index', index)
    standard_type_assertion.assert_string('file_path', file_path)

    output = codecs.open(file_path, 'w', 'utf-8-sig')
    for path, data in index.getPairList():
        output.write(str(data.getMtime()))
        output.write(' ')
        output.write(data.getHash())
        output.write(' ')
        output.write(path)
        output.write('\n')
    output.close()


def update_index_file(tree_path, index_path, skip_paths):
    standard_type_assertion.assert_string('tree_path', tree_path)
    standard_type_assertion.assert_string('index_path', index_path)

    if os.path.isfile(index_path):
        old_index = load_index(index_path)
        new_index = update_index(old_index, tree_path, skip_paths)
    else:
        new_index = create_index(tree_path, skip_paths)
    save_index(new_index, index_path)
