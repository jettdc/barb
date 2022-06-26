import os.path
from enum import Enum
import stat


class Hook(Enum):
    PRE_COMMIT = 'pre-commit'


def _hook_exists(hook_type: Hook):
    return os.path.exists(f'./.git/hooks/{hook_type.value}')


def _make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(path, mode)


def _make_hook(hook_type: Hook, script):
    path = f'./.git/hooks/{hook_type.value}'
    with open(path, 'w') as file:
        file.write(script)

    _make_executable(path)


def add(hook_type: Hook, script):
    # if _hook_exists(hook_type):
    #     raise Exception(f"Hook {hook_type} already exists, cannot register.")

    _make_hook(hook_type, script)
