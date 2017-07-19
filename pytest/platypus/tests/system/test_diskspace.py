import logging
import pytest
import subprocess

LOG = logging.getLogger(__name__)

fstypes = [
    'ext2',
    'ext3',
    'ext4',
    'xfs',
    'btrfs'
]

with open('/proc/mounts', 'r') as fd:
    mountpoints = [mount[1] for mount in
                   [line.strip().split() for line in fd]
                   if mount[2] in fstypes]

@pytest.mark.parametrize('path', mountpoints)
def test_diskspace(path):
    out = subprocess.check_output([
        'df', '--output=target,pcent', path])

    target, pcent = out.splitlines()[1].split()
    pcent = int(pcent[:-1])

    LOG.info('filesystem at %s is %s%% full',
             target, pcent)

    assert pcent < 80, 'diskspace: filesystem at %s is %s%% full' % (
        target, pcent)
