import logging
import pytest

LOG = logging.getLogger(__name__)

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None

try:
    import oslo_config
    import oslo_config.cfg
except ImportError:
    oslo_config = None


@pytest.mark.skipif(sqlalchemy is None,
                    reason='keystone: sqlalchemy is not available')
@pytest.mark.skipif(oslo_config is None,
                    reason='keystone: oslo_config is not available')
def test_keystone_token_table(keystone_token_limit, keystone_config_files):
    conf = oslo_config.cfg.ConfigOpts()
    conf.register_opt(
        oslo_config.cfg.StrOpt('connection',
                               deprecated_group='DEFAULT',
                               deprecated_name='sql_connection'),
        group='database')

    conf(args=[],
         project='keystone',
         default_config_files=keystone_config_files)

    connection = conf.database.connection
    LOG.info('connecting to keystone database at %s',
             connection)

    assert connection is not None, (
        'keystone: database connection is undefined')

    engine = sqlalchemy.create_engine(connection)
    try:
        res = engine.execute('select count(id) from token')
    except sqlalchemy.exc.DatabaseError as err:
        pytest.fail('keystone: database query failed: %s' % (err,))
    count = res.first()[0]

    LOG.info('found %d tokens in token table', count)

    assert count < keystone_token_limit, (
        'keystone: token table is large; is your expiration job running?')
