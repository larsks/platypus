import pytest

try:
    import oslo_config
    import oslo_config.cfg
except ImportError:
    oslo_config = None

def pytest_generate_tests(metafunc):
    if oslo_config is None:
        return

    config_files = metafunc.config.option.cinder_config_file

    conf = oslo_config.cfg.ConfigOpts()
    conf.register_opt(
        oslo_config.cfg.ListOpt('enabled_backends'))

    conf(project='cinder',
         args=[],
         default_config_files=config_files)

    metafunc.parametrize('cinder_conf', [conf])

    if 'cinder_backend' in metafunc.fixturenames:
        enabled_backends = filter(None, conf.enabled_backends or [])
        for backend in enabled_backends:
            conf.register_opt(
                oslo_config.cfg.StrOpt('volume_driver'), group=backend)

        metafunc.parametrize('cinder_backend', enabled_backends)


@pytest.fixture
def cinder_conf():
    pass

@pytest.fixture
def cinder_backend():
    pass
