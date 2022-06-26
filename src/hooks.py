import os.path
from enum import Enum


class Hook(Enum):
    PRE_COMMIT = 'pre-commit'


def _hook_exists(hook_type: Hook):
    return os.path.exists(f'./.git/hooks/{hook_type.value}')


def _make_hook(hook_type: Hook, script):
    with open(f'./.git/hooks/{hook_type.value}', 'w') as file:
        file.write("""
        #!/bin/sh
        
        py-hook run pre-commit
        """)


def add(hook_type: Hook, script):
    # if _hook_exists(hook_type):
    #     raise Exception(f"Hook {hook_type} already exists, cannot register.")

    _make_hook(hook_type, script)
