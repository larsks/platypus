import pytest
import subprocess

def get_cluster_properties():
    props = {}
    res = subprocess.check_output(['pcs', 'property', 'list', '--all'])
    for line in res.splitlines():
        if line == 'Cluster Properties:':
            continue

        prop, _, val = line.partition(': ')
        props[prop.strip()] = val

    return props

def test_fencing_configured():
    try:
        subprocess.check_call(['pcs', 'status'])
    except (OSError, subprocess.CalledProcessError):
        pytest.skip('pacemaker: pacemaker is not running on this node')

    props = get_cluster_properties()
    assert props.get('stonith-enabled', 'false') is not 'false', (
        'pacemaker: fencing is explicitly disabled')

    res = subprocess.check_output(['pcs', 'stonith', 'show'])
    for line in res.splitlines():
        assert line != 'NO stonith devices configured', (
            'pacemaker: fencing is not confiugred')

        fields = line.split()
        assert fields[-1] != 'Stopped', (
            'pacemaker: fencing device %s is stopped' % fields[0])
