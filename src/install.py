from .hooks import Hook, add


def _get_base_hook(name: str) -> str:
    return f'#!/bin/sh\n\nbarb run {name}\n'


def install_base_hooks():
    for hook in Hook:
        add(hook, _get_base_hook(hook.value))
