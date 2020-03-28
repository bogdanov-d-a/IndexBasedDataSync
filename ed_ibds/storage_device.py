import ed_ibds.standard_type_assertion


class StorageDevice:
    def __init__(self, name, is_removable, is_scan_available):
        ed_ibds.standard_type_assertion.assert_string('name', name)
        ed_ibds.standard_type_assertion.assert_bool('is_removable', is_removable)
        ed_ibds.standard_type_assertion.assert_bool('is_scan_available', is_scan_available)

        self._name = name
        self._is_removable = is_removable
        self._is_scan_available = is_scan_available

    def getName(self):
        return self._name

    def isRemovable(self):
        return self._is_removable

    def isScanAvailable(self):
        return self._is_scan_available


def assert_storage_device(name, data):
    if type(data) is not StorageDevice:
        raise TypeError(name + ' should be StorageDevice')
