from typing import List
from enum import Enum
import os.path
import stat


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


def _make_executable(path: str):
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)


def add(hook_type: Hook, script: str):
    path = f'./.git/hooks/{hook_type.value}'
    with open(path, 'w', newline='\n') as file:
        file.write(script)

    _make_executable(path)
