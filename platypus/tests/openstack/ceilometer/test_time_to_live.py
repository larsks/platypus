import pytest

def test_ceilometer_time_to_live(ceilometer_conf):
    if ceilometer_conf is None:
        pytest.skip('ceilometer: ceilometer configuration is not available')

    ttl = (ceilometer_conf.database.metering_time_to_live
           or ceilometer_conf.database.time_to_live)

    assert ttl is not None, (
        'ceilometer: metering_time_to_live is not set')
    assert ttl > 0, (
        'ceilometer: metering_time_to_live is infinite')
