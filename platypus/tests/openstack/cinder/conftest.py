from __future__ import print_function
import pytest

try:
    from cinder.common.config import CONF
    from cinder.objects import volume
    from cinder.objects import volume_attachment

    try:
        from cinder.volume.manager import volume_backend_opts
    except ImportError:
        from cinder.volume.manager import volume_manager_opts as volume_backend_opts
except ImportError:
    CONF = None

def pytest_generate_tests(metafunc):
    if CONF is None:
        return

    CONF(project='cinder',
         args=metafunc.config.option.cinder_arg)

    metafunc.parametrize('cinder_conf', [CONF])

    if 'cinder_backend' in metafunc.fixturenames:
        enabled_backends = filter(None, CONF.enabled_backends or [])
        for backend in enabled_backends:
            CONF.register_opts(volume_backend_opts, group=backend)

        metafunc.parametrize('cinder_backend', enabled_backends)


@pytest.fixture
def cinder_conf():
    pass

@pytest.fixture
def cinder_backend():
    pass

