import pytest
import subprocess

try:
    from oslo_config import cfg

    debug_opt = cfg.BoolOpt('debug', default=False)
    configfiles = [cfgfile for cfgfile in
                   subprocess.check_output([
                       'rpm', '-qa', '--configfiles', 'openstack*']).splitlines()
                   if cfgfile.startswith('/etc') and cfgfile.endswith('.conf')]
except ImportError:
    cfg = None
    configfiles = []

@pytest.mark.skipif(cfg is None,
                    reason='debug_logs: oslo_config is not available')
@pytest.mark.parametrize('path', configfiles)
def test_debug_logging(path):
    CONF = cfg.ConfigOpts()
    CONF.register_opt(debug_opt)

    try:
        CONF(args=['--config-file', path])
    except cfg.ConfigFileParseError:
        pytest.skip('debug_logs: cannot parse %s' % path)

    assert CONF.debug is False, (
        'debug_logs: debug logging is enabled in %s' % path)
