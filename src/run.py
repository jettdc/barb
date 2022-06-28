import importlib.util
import os.path
import subprocess
import sys
from src.config import Config
import platform
from src.hooks import Hook
from src.logger import Logger

log = Logger.get_logger()


def _get_hook_path(hook: str):
    if not os.path.exists(f'./.barb/{hook}') and not os.path.exists(f'./.barb/{hook}.py'):
        return None

    if os.path.isdir(f'./.barb/{hook}'):
        files = os.listdir(f'./.barb/{hook}')
        op_sys = platform.system()

        for file in files:
            filename, ext = os.path.splitext(file)
            if filename.lower() == op_sys.lower():
                return f'./.barb/{hook}/{file}'

        return None

    return f'./.barb/{hook}'


def _get_exec_program() -> str:
    config = Config.get_instance()
    operating_system = config.config.current_os
    if operating_system == 'linux' or operating_system == 'darwin':
        return 'bash'
    elif operating_system == 'windows':
        return config.config.windows_interpreter
    else:
        log.error("Unsupported operating system.")


def _execute_shell_hook(hook_path: str, args):
    try:
        new_hook_path = hook_path
        for arg in args:
            new_hook_path += f' {str(arg)}'
        interpreter_args = Config.get_instance().config.interpreter_args
        process_result = subprocess.run([_get_exec_program()] + interpreter_args + [new_hook_path], shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, timeout=2)

        if process_result.returncode != 0:
            log.error('Failed to run the git hook script.')
            if process_result.stderr:
                log.error(process_result.stderr.decode())
            sys.exit(1)

        if process_result.stdout:
            log.info(process_result.stdout.decode())

        # subprocess.run([_get_exec_program(), new_hook_path])
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
