from __future__ import print_function
import pytest
import sys

try:
    import oslo_config
    import oslo_config.cfg
except ImportError:
    oslo_config = None

@pytest.fixture
def keystone_token_limit(request):
    return int(request.config.getoption('--keystone-token-limit'))

@pytest.fixture
def keystone_config_files(request):
    return request.config.getoption('--keystone-config-file')
