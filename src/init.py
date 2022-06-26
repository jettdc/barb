from .install import install_base_hooks
import os


def _is_initialized():
    return os.path.isdir('./.barb')


def _initialize():
    os.mkdir('.barb')
    install_base_hooks()


def init():
    if _is_initialized():
        print('barb already initialized. To install the hooks, run\n\tbarb install')
        return

    _initialize()
