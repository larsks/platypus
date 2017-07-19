import logging

logging.basicConfig(level='INFO')

def pytest_addoption(parser):
    parser.addoption('--mongo-storage-limit',
                     default=1e+9,
                     type=int)
    parser.addoption('--keystone-token-limit',
                     default=10000,
                     type=int)
    parser.addoption('--keystone-config-file',
                     action='append')
    parser.addoption('--cinder-config-file',
                     action='append')
    parser.addoption('--ceilometer-config-file',
                     action='append')
