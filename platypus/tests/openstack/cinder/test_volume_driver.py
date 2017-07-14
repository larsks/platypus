from __future__ import print_function
import pytest

def test_cinder_volume_driver(cinder_conf, cinder_backend):
    if cinder_conf is None:
        pytest.skip('cinder: cinder configuration is not available')

    volume_driver = getattr(cinder_conf, cinder_backend).volume_driver

    assert volume_driver is not None, (
        'cinder: backend %s has no volume_driver configured' % cinder_backend)
    assert not volume_driver.endswith('LVMVolumeDriver'), (
        'cinder: backend %s uses the LVM volume driver, '
        'which is not recommended' % cinder_backend)
