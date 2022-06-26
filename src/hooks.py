import os.path
from enum import Enum
import stat
from pathlib import Path


class Hook(Enum):
    PRE_COMMIT = 'pre-commit'


def _hook_exists(hook_type: Hook):
    return os.path.exists(f'./.git/hooks/{hook_type.value}')


def get_umask():
    umask = os.umask(0)
    os.umask(umask)
    return umask


def _make_executable(path):
    os.chmod(
        path,
        os.stat(path).st_mode |
        (
                (
                        stat.S_IXUSR |
                        stat.S_IXGRP |
                        stat.S_IXOTH
                )
                & ~get_umask()
        )
    )


def _make_hook(hook_type: Hook, script):
    path = f'./.git/hooks/{hook_type.value}'
    with open(path, 'w') as file:
        file.write(script)

    _make_executable(path)


def add(hook_type: Hook, script):
    # if _hook_exists(hook_type):
    #     raise Exception(f"Hook {hook_type} already exists, cannot register.")

    _make_hook(hook_type, script)
