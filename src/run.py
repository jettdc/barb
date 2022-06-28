import importlib.util
import os.path
import subprocess
import sys
import platform
from src.hooks import Hook
from src.logger import Logger

log = Logger.get_logger()


def _get_hook_path(hook: str):
    if not os.path.exists(f'./.barb/{hook}') and not os.path.exists(f'./.barb/{hook}.py'):
        return None

    if os.path.isdir(f'./.barb/{hook}'):

        op_sys = platform.system()
        if op_sys == 'Linux' and os.path.isfile(f'./.barb/{hook}/linux'):
            return f'./.barb/{hook}/linux'
        elif op_sys == 'Linux' and os.path.isfile(f'./.barb/{hook}/linux.py'):
            return f'./.barb/{hook}/linux.py'
        elif op_sys == 'Windows' and os.path.isfile(f'./.barb/{hook}/windows'):
            return f'./.barb/{hook}/windows'
        elif op_sys == 'Windows' and os.path.isfile(f'./.barb/{hook}/windows.py'):
            return f'./.barb/{hook}/windows.py'
        elif op_sys == 'Darwin' and os.path.isfile(f'./.barb/{hook}/darwin'):
            return f'./.barb/{hook}/darwin'
        elif op_sys == 'Darwin' and os.path.isfile(f'./.barb/{hook}/darwin.py'):
            return f'./.barb/{hook}/darwin.py'

    elif os.path.isfile(f'./.barb/{hook}'):
        return f'./.barb/{hook}'
    elif os.path.isfile(f'./.barb/{hook}.py'):
        return f'./.barb/{hook}.py'
    else:
        return None


def _get_exec_program() -> str:
    operating_system = platform.system()
    if operating_system == 'Linux' or operating_system == 'Darwin':
        return 'bash'
    elif operating_system == 'Windows':
        return 'powershell'
    else:
        log.error("Unsupported operating system.")


def _execute_shell_hook(hook_path: str, args):
    try:
        new_hook_path = hook_path
        for arg in args:
            new_hook_path += f' {str(arg)}'

        subprocess.run([_get_exec_program(), new_hook_path])
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
