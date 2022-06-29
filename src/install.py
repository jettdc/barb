from .hooks import Hook, add, get_args_for_hook
import os


def _get_base_hook(name: str, nargs: int) -> str:
    args = ''
    for i in range(nargs):
        args += f' ${i + 1}'

    return f'#!/bin/sh{os.linesep}{os.linesep}barb run {name}{args}{os.linesep}'


def install_base_hooks():
    for hook in Hook:
        add(hook, _get_base_hook(hook.value, len(get_args_for_hook(hook))))
    return True
