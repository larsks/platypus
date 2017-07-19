import logging
import pytest
import subprocess

try:
    import oslo_config
    import oslo_config.cfg

    configfiles = [cfgfile for cfgfile in
                   subprocess.check_output([
                       'rpm', '-qa', '--configfiles', 'openstack*']).splitlines()
                   if cfgfile.startswith('/etc') and cfgfile.endswith('.conf')]
except ImportError:
    oslo_config = NOne
    configfiles = []

LOG = logging.getLogger(__name__)


@pytest.mark.skipif(oslo_config is None,
                    reason='debug_logs: oslo_config is not available')
@pytest.mark.parametrize('path', configfiles)
def test_debug_logging(path):
    conf = oslo_config.cfg.ConfigOpts()
    conf.register_opt(oslo_config.cfg.BoolOpt('debug', default=False))

    LOG.info('parsing file %s', path)

    try:
        conf(args=[],
             default_config_files=[path])
    except oslo_config.cfg.ConfigFileParseError:
        pytest.skip('debug_logs: cannot parse %s' % path)

    assert conf.debug is False, (
        'debug_logs: debug logging is enabled in %s' % path)
