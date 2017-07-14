
def pytest_addoption(parser):
    parser.addoption('--keystone-token-limit',
                     default=10000)
    parser.addoption('--keystone-arg',
                     action='append',
                     default=[])
    parser.addoption('--cinder-arg',
                     action='append',
                     default=[])
    parser.addoption('--ceilometer-arg',
                     action='append',
                     default=[])

