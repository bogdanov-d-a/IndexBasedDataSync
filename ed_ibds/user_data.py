import ed_ibds.standard_type_assertion
import ed_ibds.storage_device


class UserData:
    def __init__(self, collection_dict, device_list, data_path):
        if type(collection_dict) is not dict:
            raise TypeError('collection_dict should be dict')
        ed_ibds.standard_type_assertion.assert_list('device_list', device_list, ed_ibds.storage_device.assert_storage_device)
        ed_ibds.standard_type_assertion.assert_string('data_path', data_path)

        self._collection_dict = collection_dict
        self._device_list = device_list
        self._data_path = data_path

    def getCollectionDict(self):
        return self._collection_dict

    def getDeviceList(self):
        return self._device_list

    def getDataPath(self):
        return self._data_path
