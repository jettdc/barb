import sys

from dotenv import load_dotenv
from src.version import VERSION
import os


def _verify_version_change():
    with open('./.barb/pre-push-cache.txt', 'r') as f:
        return f.readline() != VERSION


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

    if not _version_cache_exists():
        _create_version_cache(VERSION)
    else:
        if not _verify_version_change():
            print('Package version number has not been changed since last push. Cancelling.')
            sys.exit(1)
