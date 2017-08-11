import standard_type_assertion
import user_interaction
import os
import ibds_utils


def assert_storage_device(name, data):
    if type(data) is not StorageDevice:
        raise TypeError(name + ' should be StorageDevice')


class StorageDevice:
    _PC = 'PC'
    _UMS = 'UMS'

    _DEVICES = set([_PC, _UMS])
    _DEVICES_REMOVABLE = set([_UMS])

    def __init__(self, name):
        standard_type_assertion.assert_string('name', name)
        if name not in StorageDevice._DEVICES:
            raise Exception('Bad device name')
        self._name = name

    def getName(self):
        return self._name

    def isRemovable(self):
        return self._name in StorageDevice._DEVICES_REMOVABLE


class Location:
    def __init__(self, storage_device, path, is_complete):
        assert_storage_device('storage_device', storage_device)
        standard_type_assertion.assert_string('path', path)
        standard_type_assertion.assert_bool('is_complete', is_complete)

        self._storage_device = storage_device
        self._path = path
        self._is_complete = is_complete

    def getStorageDevice(self):
        return self._storage_device

    def getPath(self):
        return self._path

    def isComplete(self):
        return self._is_complete


COLLECTION_MAP = {
    'Documents': [
        Location(StorageDevice('PC'), 'C:\\Documents', True),
        Location(StorageDevice('UMS'), 'Documents', False),
    ],
}


def locations_to_storage_devices(locations):
    return list(map(lambda x: x.getStorageDevice(), locations))


def _str_from_suffix(obj):
    if type(obj) is str:
        return obj
    elif type(obj) is StorageDevice:
        return obj.getName()
    else:
        raise Exception('unknown object type')


DATA_DIR = 'data'


def gen_index_file_path(collection, suffix, is_path=True):
    standard_type_assertion.assert_string('collection', collection)

    prefix = ''
    if is_path:
        prefix = DATA_DIR + '\\'

    return prefix + collection + '-' + _str_from_suffix(suffix) + '.txt'


def gen_common_file_path(collection, is_path=True):
    return gen_index_file_path(collection, 'Common', is_path)


def gen_hashset_file_path(collection, is_path=True):
    return gen_index_file_path(collection, 'Hashset', is_path)


def pick_storage_device():
    list_ = sorted(list(StorageDevice._DEVICES))
    return StorageDevice(list_[user_interaction.pick_option('Choose storage device', list_)])


def generate_target_file_list():
    list_ = []

    for name, locations in COLLECTION_MAP.items():
        for location in locations:
            list_.append(gen_index_file_path(name, location.getStorageDevice(), False))
        list_.append(gen_common_file_path(name, False))
        list_.append(gen_hashset_file_path(name, False))

    return list_


def generate_actual_file_list():
    return os.listdir(DATA_DIR)


def check_data_file_set():
    target = set(generate_target_file_list())
    actual = set(generate_actual_file_list())
    ibds_utils.print_lists([['Odd', actual - target], ['Missing', target - actual]])
