from .install import install_base_hooks
import os


def _is_initialized():
    return os.path.isdir('./.py-hook')

def _initialize():
    os.mkdir('.py-hook')
    install_base_hooks()


def init():
    if _is_initialized():
        print('py-hook already initialized. To install the hooks, run\n\tpy-hook install')
        return

    _initialize()
