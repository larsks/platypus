from __future__ import print_function
import pytest

try:
    import ceilometer
    from ceilometer import opts as global_opts
    from ceilometer.storage import OPTS as storage_opts
    from oslo_db import options as db_options
    from oslo_config import cfg
except ImportError:
    ceilometer = None

@pytest.fixture
def ceilometer_args(request):
    return request.config.getoption('--ceilometer-arg')

@pytest.fixture
def ceilometer_conf(request, ceilometer_args):
    if ceilometer is None:
        return

    conf = cfg.ConfigOpts()
    for group, options in global_opts.list_opts():
        conf.register_opts(list(options),
                           group=None if group == "DEFAULT" else group)

    conf.register_opts(storage_opts, group='database')
    db_options.set_defaults(conf)

    conf(ceilometer_args, project='ceilometer')
    return conf

@pytest.fixture
def mongo_storage_limit(request):
    return request.config.getoption('--mongo-storage-limit')
