from __future__ import print_function
import pytest
import sys

try:
    from keystone.conf import CONF
except ImportError:
    CONF = None

def pytest_addoption(parser):
    parser.addoption('--keystone-token-limit',
                     default=10000)
    parser.addoption('--keystone-arg',
                     action='append',
                     default=[])

@pytest.fixture
def keystone_args(request):
    return request.config.getoption('--keystone-arg')

@pytest.fixture
def keystone_conf(request, keystone_args):
    if CONF is None:
        return

    CONF(project='keystone', args=keystone_args)
    return CONF

@pytest.fixture
def keystone_token_limit(request):
    return int(request.config.getoption('--keystone-token-limit'))