import os.path
from enum import Enum
import stat
from pathlib import Path


class Hook(Enum):
    PRE_COMMIT = 'pre-commit'


def _hook_exists(hook_type: Hook):
    return os.path.exists(f'./.git/hooks/{hook_type.value}')


def _make_executable(path):
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)


def _make_hook(hook_type: Hook, script):
    path = f'./.git/hooks/{hook_type.value}'
    with open(path, 'w') as file:
        file.write(script)

    _make_executable(path)


def add(hook_type: Hook, script):
    # if _hook_exists(hook_type):
    #     raise Exception(f"Hook {hook_type} already exists, cannot register.")

    _make_hook(hook_type, script)
