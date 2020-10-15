""" Fixtures for LocalId module tests
"""
from unittest.mock import Mock
from urllib.parse import urljoin

from tests import test_settings


class MockResponse(object):
    def __init__(self, text, status_code):
        self.status_code = status_code
        self.text = text


class MockPID(object):
    def __init__(self, host_url=None, provider=None, prefix=None, value=None):
        self.host_url = test_settings.SERVER_URI if host_url is None else host_url
        self.provider = (
            list(test_settings.ID_PROVIDER_SYSTEMS.keys())[0]
            if provider is None
            else provider
        )
        self.prefix = "mock_prefix" if prefix is None else prefix
        self.value = "mock_record" if value is None else value

    def __str__(self):
        return urljoin(
            self.host_url,
            "pid/%s/%s/%s"
            % (
                self.provider,
                self.prefix,
                self.value,
            ),
        )


class MockProvider(object):
    def __init__(self):
        self.provider_url = str(MockPID(prefix="", value=""))[:-1]


def mock_return_fn_args_as_dict(*args, **kwargs):
    kwargs.update({"arg%d" % i: args[i] for i in range(len(args))})

    return kwargs
