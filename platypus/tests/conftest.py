
def pytest_addoption(parser):
    parser.addoption('--mongo-storage-limit',
                     default=1e+9,
                     type=int)
    parser.addoption('--keystone-token-limit',
                     default=10000,
                     type=int)
    parser.addoption('--keystone-arg',
                     action='append',
                     default=[])
    parser.addoption('--cinder-arg',
                     action='append',
                     default=[])
    parser.addoption('--ceilometer-arg',
                     action='append',
                     default=[])

