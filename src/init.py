from src.install import install_base_hooks
from src.logger import Logger
import os

log = Logger.get_logger()

def _is_initialized():
    return os.path.isdir('./.barb')


def _is_git_repo():
    return os.path.isdir('./.git')


def _has_barb_dir():
    return os.path.isdir('./.barb')


def _has_barbrc():
    return os.path.exists('./.barbrc.toml')


def _initialize():
    if not _has_barb_dir():
        os.mkdir('.barb')

    if not _has_barbrc():
        with open('./.barbrc.toml', 'w') as f:
            f.write('\n')

    install_base_hooks()


def init():
    if not _is_git_repo():
        log.error('No existing git repository found. Type "git init" to initialize one.')
        return False

    if _is_initialized():
        log.error('Already initialized. To install the hooks, run\n\tbarb install')
        return False

    _initialize()

    return True

