from importlib.machinery import SourceFileLoader
from dotenv import load_dotenv
import subprocess
import sys
import os


def _verify_version_change(v):
    with open('./.barb/version-cache', 'r') as f:
        return f.readline() != v


def _version_cache_exists():
    return os.path.exists('./.barb/version-cache')


def _write_version_cache(version):
    with open('./.barb/pre-push-cache.txt', 'w') as f:
        f.write(version)


def hook(stdin, *args):
    pushing_to = sys.stdin.readline().split(" ")[2]

    print("Pre hook for push to", pushing_to)

    if pushing_to != 'refs/heads/main':
        print("Skipping publish since not pushing to main.")
        return

    pypi_usr, pypi_pwd = os.environ.get('PYPI_USERNAME'), os.environ.get('PYPI_PASSWORD')

    if pypi_usr is None or pypi_pwd is None:
        print('Skipping PyPi publish because PyPi credentials are missing from the environment.')

    print('Publishing barb to PyPi:')

    module = SourceFileLoader("version", "./src/version.py").load_module()
    v = module.VERSION
    if not _version_cache_exists():
        _write_version_cache(v)
    else:
        print('Verifying package version number change.')
        if not _verify_version_change(v):
            print('Package version number has not been changed since last push. Cancelling.')
            sys.exit(1)

        _write_version_cache(v)

    print("Attempting to build and upload...")
    subprocess.run(['bash', './publish.sh', pypi_usr, pypi_pwd])

    print("Successfully published the package.")
