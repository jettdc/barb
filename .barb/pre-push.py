import os

from dotenv import load_dotenv

def _verify_version_change():
    pass

def hook(*args):
    print('hok')
    print(*args)
    load_dotenv()

    pypi_usr, pypi_pwd = os.environ.get('PYPI_USERNAME'), os.environ.get('PYPI_PASSWORD')

    if pypi_usr is None or pypi_pwd is None:
        print('Skipping PyPi publish because PyPi credentials are missing from the environment.')

    print('Publishing barb to PyPi:')
