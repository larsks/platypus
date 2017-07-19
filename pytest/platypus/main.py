import os
import sys
import pytest

HERE = os.path.dirname(__file__)

def main():
    args = sys.argv[1:]
    args.append('--assert=plain')
    args.append(os.path.join(HERE, 'tests'))

    sys.exit(pytest.main(args))
