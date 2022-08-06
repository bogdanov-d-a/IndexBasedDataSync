from . import standard_type_assertion
from . import storage_device


class UserData:
    def __init__(self, collection_dict, device_list, data_path, skip_mtime):
        standard_type_assertion.assert_dict('collection_dict', collection_dict)
        standard_type_assertion.assert_list_pred('device_list', device_list, storage_device.assert_storage_device)
        standard_type_assertion.assert_string('data_path', data_path)
        standard_type_assertion.assert_bool('skip_mtime', skip_mtime)

        self._collection_dict = collection_dict
        self._device_list = device_list
        self._data_path = data_path
        self._skip_mtime = skip_mtime

    def getCollectionDict(self):
        return self._collection_dict

    def getDeviceList(self):
        return self._device_list

    def getDataPath(self):
        return self._data_path

    def getSkipMtime(self):
        return self._skip_mtime
