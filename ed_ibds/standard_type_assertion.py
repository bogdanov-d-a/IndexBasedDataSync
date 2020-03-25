def assert_string(name, data):
    if type(data) is not str:
        raise TypeError(name + ' should be string')


def assert_list(name, data, assert_elem=lambda name, data: None):
    if type(data) is not list:
        raise TypeError(name + ' should be list')
    for elem in data:
        assert_elem(name + ' elem', elem)


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
