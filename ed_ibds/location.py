from . import standard_type_assertion
from . import storage_device


class Location:
    def __init__(self, storage_device_, path, is_complete):
        storage_device.assert_storage_device('storage_device_', storage_device_)
        standard_type_assertion.assert_string('path', path)
        standard_type_assertion.assert_bool('is_complete', is_complete)

        self._storage_device = storage_device_
        self._path = path
        self._is_complete = is_complete

    def getStorageDevice(self):
        return self._storage_device

    def getPath(self):
        return self._path

    def isComplete(self):
        return self._is_complete
