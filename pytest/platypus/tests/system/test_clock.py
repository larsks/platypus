import logging
import subprocess

LOG = logging.getLogger(__name__)


def test_ntp_offset():
    '''Test that local NTP offset is < 1 second.'''

    active_ntp_service = None

    for svc in ['chronyd', 'ntpd']:
        try:
            # we call check_output here in order to discard the
            # output from systemctl is-active.
            subprocess.check_output(['systemctl', 'is-active', svc])
            active_ntp_service = svc
            LOG.info('found active ntp service = %s', svc)
            break
        except subprocess.CalledProcessError as exc:
            continue

    if active_ntp_service == 'chronyd':
        offset = _ntp_offset_chronyd()
    elif active_ntp_service == 'ntpd':
        offset = _ntp_offset_ntpd()
    else:
        assert False, 'ntp: no ntp service is active on this host.'

    if offset is not None:
        LOG.info('ntp clock offset = %f', offset)

    assert offset is not None, 'ntp: clock is not synchronized'
    assert offset < 1, 'ntp: offset is too large (>= 1)'

def _ntp_offset_chronyd():
    try:
        out = subprocess.check_output(['chronyc', 'tracking'])
    except subprocess.CalledProcessError:
        return None

    data = {x[0].strip(): x[2].strip()
           for x in [line.partition(':')
                     for line in out.splitlines()]}

    return float(data['RMS offset'].split()[0])

def _ntp_offset_ntpd():
    try:
        out = subprocess.check_output(['ntpq', '-c', 'peers'])
    except subprocess.CalledProcessError:
        return None

    for line in out.splitlines():
        if line.startswith('*'):
            break
    else:
        return None

    data = line.split()
    offset = data[7]
    return float(offset)/1000
