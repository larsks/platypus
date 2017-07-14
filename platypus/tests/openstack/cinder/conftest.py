from __future__ import print_function
import pytest

try:
    from cinder.common.config import CONF
except ImportError:
    CONF = None

def pytest_addoption(parser):
    parser.addoption('--cinder-arg',
                     action='append',
                     default=[])

def pytest_generate_tests(metafunc):
    if CONF is None:
        return

    CONF(project='cinder',
         args=metafunc.config.option.cinder_arg)

    if 'cinder_backend' in metafunc.fixturenames:
        enabled_backends = CONF.enabled_backends or []
        metafunc.parametrize('cinder_backend',
                              filter(None, enabled_backends))
