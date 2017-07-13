import sys
import pytest

def main():
    args = sys.argv[1:]
    args.append('--assert=plain')
    args.extend(['--pyargs', __name__.split('.')[0]])
    print args
    pytest.main(args)
