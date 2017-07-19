import pytest

try:
    import oslo_config
    import oslo_config.cfg
except ImportError:
    oslo_config = None


@pytest.fixture
def ceilometer_conf(request):
    if oslo_config is None:
        return

    conf = oslo_config.cfg.ConfigOpts()

    conf.register_opt(
        oslo_config.cfg.StrOpt('metering_connection',
                               deprecated_name='connection'),
        group='database')

    conf.register_opt(
        oslo_config.cfg.IntOpt('metering_time_to_live',
                               deprecated_name='time_to_live'),
        group='database')

    config_files = request.config.getoption('--ceilometer-config-file')
    conf(project='ceilometer',
         args=[],
         default_config_files=config_files)

    return conf

@pytest.fixture
def mongo_storage_limit(request):
    return request.config.getoption('--mongo-storage-limit')
