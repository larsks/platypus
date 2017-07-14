import pytest

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None

try:
    import oslo_db
    import oslo_db.options
except ImportError:
    oslo_db = None

@pytest.mark.skipif(sqlalchemy is None,
                    reason='keystone: sqlalchemy is not available')
@pytest.mark.skipif(oslo_db is None,
                    reason='keystone: oslo_db is not available')
def test_keystone_token_table(keystone_conf, keystone_token_limit):
    if keystone_conf is None:
        pytest.skip('keystone: no keystone configuration available')

    oslo_db.options.set_defaults(keystone_conf)
    assert keystone_conf.database.connection is not None, (
        'keystone: database connection is undefined')

    engine = sqlalchemy.create_engine(keystone_conf.database.connection)
    res = engine.execute('select count(id) from token')
    count = res.first()[0]

    assert count < keystone_token_limit, (
        'keystone: token table is large; is your expiration job running?')
