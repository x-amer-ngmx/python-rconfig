import os
from unittest import mock

from rconfig import _set_environment_variables


@mock.patch.dict(os.environ, dict(), clear=True)
def test_subprocess_env():
    data = {
        'RCONFIG_TEST_INT': 1,
        'RCONFIG_TEST_STR': 'TEST',
        'RCONFIG_TEST_BOOL': True,
        'RCONFIG_TEST_LIST': [1, 'Test', True],
        'RCONFIG_TEST_DICT': {'test1': 1, 'test2': 'TEST', 'test3': True},

    }
    _set_environment_variables(data)
    assert os.environ['RCONFIG_TEST_INT'] == '1'
    assert os.environ['RCONFIG_TEST_STR'] == 'TEST'
    assert os.environ['RCONFIG_TEST_BOOL'] == 'true'
    assert os.environ['RCONFIG_TEST_LIST'] == '[1, "Test", true]'
    assert os.environ['RCONFIG_TEST_DICT'] == \
        '{"test1": 1, "test2": "TEST", "test3": true}'


@mock.patch.dict(os.environ, dict(), clear=True)
def test_subprocess_env_prefix():
    data = {
        'RCONFIG_TEST_INT': 1,
        'RCONFIG_TEST_STR': 'TEST',
        'RCONFIG_TEST_BOOL': True,
        'RCONFIG_TEST_LIST': [1, 'Test', True],
        'RCONFIG_TEST_DICT': {'test1': 1, 'test2': 'TEST', 'test3': True},

    }
    _set_environment_variables(data, 'PREFIX_')
    assert os.environ['PREFIX_RCONFIG_TEST_INT'] == '1'
    assert os.environ['PREFIX_RCONFIG_TEST_STR'] == 'TEST'
    assert os.environ['PREFIX_RCONFIG_TEST_BOOL'] == 'true'
    assert os.environ['PREFIX_RCONFIG_TEST_LIST'] == '[1, "Test", true]'
    assert os.environ['PREFIX_RCONFIG_TEST_DICT'] == \
        '{"test1": 1, "test2": "TEST", "test3": true}'
