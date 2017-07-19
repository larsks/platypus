import logging
import pytest

LOG = logging.getLogger(__name__)

try:
    import oslo_config
    import oslo_config.cfg
except ImportError:
    oslo_config = None

@pytest.mark.skipif(oslo_config is None,
                    reason='cinder: oslo_config is not available')
def test_cinder_volume_driver(cinder_conf, cinder_backend):
    volume_driver = getattr(cinder_conf, cinder_backend).volume_driver

    LOG.info('backend %s is using volume_driver %s',
             cinder_backend, volume_driver)

    assert volume_driver is not None, (
        'cinder: backend %s has no volume_driver configured' % cinder_backend)
    assert not volume_driver.endswith('LVMVolumeDriver'), (
        'cinder: backend %s uses the LVM volume driver, '
        'which is not recommended' % cinder_backend)
