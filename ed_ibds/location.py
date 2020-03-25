import ed_ibds.standard_type_assertion
import ed_ibds.storage_device


class Location:
    def __init__(self, storage_device, path, is_complete):
        ed_ibds.storage_device.assert_storage_device('storage_device', storage_device)
        ed_ibds.standard_type_assertion.assert_string('path', path)
        ed_ibds.standard_type_assertion.assert_bool('is_complete', is_complete)

        self._storage_device = storage_device
        self._path = path
        self._is_complete = is_complete

    def getStorageDevice(self):
        return self._storage_device

    def getPath(self):
        return self._path

    def isComplete(self):
        return self._is_complete
