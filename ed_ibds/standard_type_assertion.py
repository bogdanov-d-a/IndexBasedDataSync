def assert_string(name, data):
    if type(data) is not str:
        raise TypeError(name + ' should be string')


def assert_list(name, data):
    if type(data) is not list:
        raise TypeError(name + ' should be list')


def assert_list_pred(name, data, assert_elem=lambda name, data: None):
    assert_list(name, data)
    for elem in data:
        assert_elem(name + ' elem', elem)


def assert_set(name, data):
    if type(data) is not set:
        raise TypeError(name + ' should be set')


def assert_set_pred(name, data, assert_elem=lambda name, data: None):
    assert_set(name, data)
    for elem in data:
        assert_elem(name + ' elem', elem)


def assert_dict(name, data):
    if type(data) is not dict:
        raise TypeError(name + ' should be dict')


def assert_integer(name, data):
    if type(data) is not int:
        raise TypeError(name + ' should be int')


def assert_integer_gtz(name, data):
    assert_integer(name, data)
    if data <= 0:
        raise Exception(name + ' should be greater than zero')


def assert_float(name, data):
    if type(data) is not float:
        raise TypeError(name + ' should be float')


def assert_bool(name, data):
    if type(data) is not bool:
        raise TypeError(name + ' should be bool')
