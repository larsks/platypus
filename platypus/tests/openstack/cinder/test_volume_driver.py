from __future__ import print_function
import pytest

try:
    from cinder.common.config import CONF, cfg
    volume_driver_opt = cfg.StrOpt('volume_driver', default=None)
except ImportError:
    CONF = None

@pytest.mark.skipif(CONF is None,
                    reason='cinder: cinder is not available')
def test_cinder_volume_driver(cinder_backend):
    CONF.register_opt(volume_driver_opt, group=cinder_backend)
    volume_driver = getattr(CONF, cinder_backend).volume_driver
    assert volume_driver is not None, (
        'cinder: backend %s has no volume_driver configured' % cinder_backend)
    assert not volume_driver.endswith('LVMVolumeDriver'), (
        'cinder: backend %s uses the LVM volume driver, '
        'which is not recommended' % cinder_backend)
