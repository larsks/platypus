import pytest
import subprocess

configfiles = [cfgfile for cfgfile in 
               subprocess.check_output([
                   'rpm', '-qa', '--configfiles', 'openstack*']).splitlines()
               if cfgfile.startswith('/etc') and cfgfile.endswith('.conf')]

@pytest.mark.parametrize('path', configfiles)
def test_debug_logging(path):
    with open(path) as fd:
        for ln, line in enumerate(fd):
            if line.startswith('debug'):
                k, _, v = line.strip().partition('=')
                if k.strip() == 'debug':
                    assert v.lower().strip() != 'true', (
                        'debug_logs: debug logging enabled '
                        'in %s, line %d' % (path, ln+1))
