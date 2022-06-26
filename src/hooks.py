import os.path
from enum import Enum
import stat
from typing import List


class Hook(Enum):
    PRE_COMMIT = 'pre-commit'
    APPLYPATCH_MSG = 'applypatch-msg'
    PRE_APPLYPATCH = 'pre-applypatch'
    POST_APPLYPATCH = 'post-applypatch'
    PREPARE_COMMIT_MSG = 'prepare-commit-msg'
    COMMIT_MSG = 'commit-msg'
    POST_COMMIT = 'post-commit'
    PRE_REBASE = 'pre-rebase'
    POST_CHECKOUT = 'post-checkout'
    POST_MERGE = 'post-merge'
    PRE_RECEIVE = 'pre-receive'
    UPDATE = 'update'
    POST_RECEIVE = 'post-receive'
    POST_UPDATE = 'post-update'
    PRE_AUTO_GC = 'pre-auto-gc'
    POST_REWRITE = 'post-rewrite'
    PRE_PUSH = 'pre-push'


def get_hook_names() -> List[str]:
    names = []
    for attr in Hook:
        names.append(attr.value)
    return names


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
