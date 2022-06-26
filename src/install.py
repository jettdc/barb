from .hooks import Hook, add


def _get_base_hook(name: str) -> str:
    return f'#!/bin/sh\n\nbarb run {name}'


def _install(hook: Hook):
    add(hook, _get_base_hook(hook.value))


def install_base_hooks():
    for hook in Hook:
        _install(hook)
