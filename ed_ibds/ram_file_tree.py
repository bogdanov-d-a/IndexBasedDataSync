import ed_ibds.ibds_utils


class Object:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent


class File(Object):
    def __init__(self, name, parent=None):
        Object.__init__(self, name, parent)


class Directory(Object):
    def __init__(self, name, parent=None):
        Object.__init__(self, name, parent)
        self.data = {}

    def has_dir(self, name):
        if name not in self.data:
            return False
        return type(self.data[name]) is Directory

    def has_file(self, name):
        if name not in self.data:
            return False
        return type(self.data[name]) is File

    def add_dir(self, name):
        if self.has_file(name):
            raise Exception('file already exists')
        if not self.has_dir(name):
            self.data[name] = Directory(name, self)

    def add_file(self, name):
        if self.has_dir(name):
            raise Exception('dir already exists')
        if not self.has_file(name):
            self.data[name] = File(name, self)

    def add_file_path(self, path):
        if len(path) == 1:
            self.add_file(path[0])
        elif len(path) > 1:
            self.add_dir(path[0])
            subdir = self.data[path[0]]
            subdir.add_file_path(path[1:])
        else:
            raise Exception('bad path data')


def explore(tree):
    cur_dir = tree

    while True:
        for name, item in ed_ibds.ibds_utils.key_sorted_dict_items(cur_dir.data):
            if type(item) is Directory:
                print('[' + name + ']')
            else:
                print(name)

        a = input()

        if a == '/':
            break
        elif a == '..':
            if cur_dir.parent is not None:
                cur_dir = cur_dir.parent
        else:
            if cur_dir.has_dir(a):
                cur_dir = cur_dir.data[a]
