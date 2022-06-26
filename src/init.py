from .install import install_base_hooks
import os


def _is_initialized():
    return os.path.isdir('./.barb')


def _is_git_repo():
    return os.path.isdir('./.git')


def _initialize():
    os.mkdir('.barb')
    install_base_hooks()


def init():
    if not _is_git_repo():
        print('no existing git repository found. type "git init" to initialize one.')
        return

    if _is_initialized():
        print('barb already initialized. To install the hooks, run\n\tbarb install')
        return

    _initialize()
