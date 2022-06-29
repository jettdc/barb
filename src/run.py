import importlib.util
import os.path
import subprocess
import sys
from typing import Union, List, Dict
from src.config import InterpreterConfig
from src.config import Config
import platform
from src.hooks import Hook
from src.logger import Logger

log = Logger.get_logger()


def _get_hook_path(hook: str):
    for f in os.listdir('./.barb'):
        filename, ext = os.path.splitext(f)

        if filename.lower() == hook and os.path.isdir(f'./.barb/{f}'):
            files = os.listdir(f'./.barb/{f}')
            op_sys = platform.system()

            for file in files:
                filename, ext = os.path.splitext(file)
                if filename.lower() == op_sys.lower():
                    return f'./.barb/{hook}/{file}'

            return None
        elif filename.lower() == hook:
            return f'./.barb/{f}'

    return None


def _get_appropriate_interpreter(hook_path) -> InterpreterConfig:
    filename, ext = os.path.splitext(hook_path)
    config = Config.get_instance().config
    for interpreter in config.interpreters:
        if interpreter.ext.lower() == ext.lower():
            return interpreter
    return config.default_interpreter


def _execute_shell_hook(hook_path: str, args):
    try:
        new_hook_path = hook_path
        for arg in args:
            new_hook_path += f' {str(arg)}'

        interpreter = _get_appropriate_interpreter(hook_path)
        process_result = subprocess.run([interpreter.cmd] + interpreter.args + [new_hook_path], shell=False)

        if process_result.returncode != 0:
            log.error('Failed to run the git hook script.')
            if process_result.stderr:
                log.error(process_result.stderr.decode())
            sys.exit(1)

        if process_result.stdout:
            log.info(process_result.stdout.decode())

    except Exception as e:
        log.error(f'An exception occurred when attempting to execute the git hook {hook_path}.', e)
        sys.exit(1)


def _execute_python_hook(hook_path: str, args):
    spec = importlib.util.spec_from_file_location(hook_path, hook_path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)

    if not hasattr(foo, 'hook'):
        log.error('Invalid python git hook. Must have "hook" function to run.')

    try:
        res = foo.hook(*args)

        if res is not None and not res:
            log.error(f"Failure indicated by hook function in {hook_path} via return value. Aborting.")
            sys.exit(1)

    except Exception as e:
        log.error(f"Exception encountered in hook {hook_path}. Aborting.", e)
        sys.exit(1)


def run_hook(params):
    hook = params[0]

    if not Config.get_instance().os_lock_ok():
        log.error(f'Skipping git hook {hook} because current os does not match required os.')
        log.error(f'Expected {Config.get_instance().config.os_lock}, actual {Config.get_instance().config.current_os}')
        sys.exit(0)

    args = []
    if len(params) > 1:
        args = params[1:]

    hook_path = _get_hook_path(hook)
    if not hook_path:
        return None

    hook_type = "PYTHON" if hook_path.endswith(".py") else "SHELL"
    if hook_type == 'SHELL':
        _execute_shell_hook(hook_path, args)
    elif hook_type == 'PYTHON':
        _execute_python_hook(hook_path, args)
