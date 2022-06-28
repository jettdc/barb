from .hooks import Hook, add, get_args_for_hook
from typing import List


def _get_base_hook(name: str, nargs: int) -> str:
    return f'#!/bin/sh\n\nbarb run {name}{" $" * nargs}\n'


def install_base_hooks():
    for hook in Hook:
        add(hook, _get_base_hook(hook.value, len(get_args_for_hook(hook))))
