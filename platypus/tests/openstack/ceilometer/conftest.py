from __future__ import print_function
import pytest

try:
    import ceilometer
    import ceilometer.service
except ImportError:
    ceilometer = None

def pytest_addoption(parser):
    parser.addoption('--ceilometer-arg',
                     action='append',
                     default=[])

@pytest.fixture
def ceilometer_args(request):
    return request.config.getoption('--ceilometer-arg')

@pytest.fixture
def ceilometer_conf(request, ceilometer_args):
    if ceilometer is None:
        return

    conf = ceilometer.service.prepare_service(argv=ceilometer_args)
    return conf
