import os


def _is_initialized():
    return os.path.isdir('./.py-hook')


def _register_base_hooks():
    pass


def _initialize():
    os.mkdir('.py-hook')
    _register_base_hooks()


def init():
    if _is_initialized():
        return

    _initialize()
