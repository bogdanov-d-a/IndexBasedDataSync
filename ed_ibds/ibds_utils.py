import re
import edpu.user_interaction
import ed_ibds.standard_type_assertion


SKIP_PATHS_SEPARATOR = '/'


def key_sorted_dict_items(dict_):
    return sorted(dict_.items(), key=lambda t: t[0])


def print_lists(lists, name=None):
    if name is not None:
        ed_ibds.standard_type_assertion.assert_string('name', name)

    if sum(len(list_[1]) for list_ in lists) > 0:
        if name is not None:
            print(name)

        for list_ in lists:
            if len(list_[1]) == 0:
                continue

            print(list_[0])
            for line in list_[1]:
                print(line)
            print()

        print()


def is_same_list(list_):
    if len(list_) == 0:
        raise Exception('empty list is not allowed')

    for i in range(len(list_) - 1):
        if (list_[i] != list_[i + 1]):
            return False
    return True


def find_first_in_list_index(list_, pred):
    index = 0

    for elem in list_:
        if pred(elem):
            return index
        index += 1

    return -1


def path_needs_skip(path, skip_paths):
    for skip_path in skip_paths:
        if re.match(skip_path, SKIP_PATHS_SEPARATOR.join(path)) is not None:
            return True
    return False


def locations_to_storage_devices(locations):
    return list(map(lambda x: x.getStorageDevice(), locations))


def pick_storage_device(device_list):
    list_ = []
    dict_ = {}
    for device in device_list:
        if device.isScanAvailable():
            list_.append(device.getName())
            dict_[device.getName()] = device
    list_.sort()
    return dict_[list_[edpu.user_interaction.pick_option('Choose storage device', list_)]]
