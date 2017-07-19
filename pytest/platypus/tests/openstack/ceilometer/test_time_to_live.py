import logging
import pytest

LOG = logging.getLogger(__name__)

try:
    import oslo_config
    import oslo_config.cfg
except ImportError:
    oslo_config = None


@pytest.mark.skipif(oslo_config is None,
                    reason='ceilometer: oslo_config is not available')
def test_ceilometer_time_to_live(ceilometer_conf):
    ttl = ceilometer_conf.database.metering_time_to_live

    LOG.info('found metering_time_to_live = %s', ttl)

    assert ttl is not None, (
        'ceilometer: metering_time_to_live is not set')
    assert ttl > 0, (
        'ceilometer: metering_time_to_live is infinite')
