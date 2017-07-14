import json
import pytest
import subprocess
import urlparse

def test_mongodb_size(ceilometer_conf, mongo_storage_limit):
    if ceilometer_conf is None:
        pytest.skip('ceilometer: ceilometer is not available')

    connection = (ceilometer_conf.database.metering_connection
                  or ceilometer_conf.database.connection)

    if connection is None:
        pytest.skip('ceilometer: database connection is not configured')

    if not connection.startswith('mongodb:'):
        pytest.skip('ceilometer: ceilometer is not configured to use mongodb')

    url = urlparse.urlparse(connection)

    if '@' in url.netloc:
        authpart, _, hostpart = url.netloc.rpartition('@')
    else:
        authpart = None
        hostpart = url.netloc

    if authpart is not None:
        user, password = authpart.split(':')

    dbname = url.path[1:]

    cmdvec = ['mongo', '--quiet']
    if authpart:
        cmdvec.extend(['-u', user])
        cmdvec.extend(['-p', password])

    cmdvec.extend(['--eval', 'printjson(db.stats())'])

    cmdvec.append('%s/%s' % (hostpart, dbname))

    out = subprocess.check_output(cmdvec)
    data = json.loads(out)

    assert data['storageSize'] < mongo_storage_limit, (
        'ceilometer: mongodb storage is > %d GB, '
        'have you set a ttl?' % (mongo_storage_limit/1e+9))
