import json
import logging
import pytest
import subprocess
import urlparse

try:
    import pymongo
except ImportError:
    pymongo = None

try:
    import oslo_config
    import oslo_config.cfg
except ImportError:
    oslo_config = None

LOG = logging.getLogger(__name__)


@pytest.mark.skipif(oslo_config is None,
                    reason='ceilometer: oslo_config is not available')
@pytest.mark.skipif(pymongo is None,
                    reason='ceilometer: pymongo is not available')
def test_mongodb_size(ceilometer_conf, mongo_storage_limit):
    connection = ceilometer_conf.database.metering_connection

    if connection is None:
        pytest.skip('ceilometer: database connection is not configured')

    if not connection.startswith('mongodb:'):
        pytest.skip('ceilometer: ceilometer is not configured to use mongodb')

    LOG.info('connecting to mongodb at %s', connection)

    uri = urlparse.urlparse(connection)
    client = pymongo.MongoClient(connection)
    db = client[uri.path[1:]]
    data = db.eval('db.stats()')
    size = data['storageSize']

    LOG.info('storageSize of %s = %s' % (uri.path[1:], size))

    assert size < mongo_storage_limit, (
        'ceilometer: mongodb storage is > %0.2f GB, '
        'have you set a ttl?' % (mongo_storage_limit/1e+9))
