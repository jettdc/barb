import sys
from importlib.machinery import SourceFileLoader

from dotenv import load_dotenv
import os



def _verify_version_change(v):
    with open('./.barb/pre-push-cache.txt', 'r') as f:
        return f.readline() != v


def _version_cache_exists():
    return os.path.exists('./.barb/pre-push-cache.txt')


def _create_version_cache(version):
    with open('./.barb/pre-push-cache.txt', 'w') as f:
        f.write(version)


def hook(*args):
    load_dotenv()

    pypi_usr, pypi_pwd = os.environ.get('PYPI_USERNAME'), os.environ.get('PYPI_PASSWORD')

    if pypi_usr is None or pypi_pwd is None:
        print('Skipping PyPi publish because PyPi credentials are missing from the environment.')

    print('Publishing barb to PyPi:')
    module = SourceFileLoader("version","./src/version").load_module()
    v = module.version

    if not _version_cache_exists():
        _create_version_cache(v)
    else:
        if not _verify_version_change(v):
            print('Package version number has not been changed since last push. Cancelling.')
            sys.exit(1)
