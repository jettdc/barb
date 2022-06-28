import importlib.util
import os.path
import subprocess
import sys


def _get_py_hook_type(hook_type: str) -> str:
    if os.path.exists(f'./.barb/{hook_type}'):
        return 'SHELL'
    elif os.path.exists(f'./.barb/{hook_type}.py'):
        return 'PYTHON'
    else:
        return None


def _execute_shell_hook(hook_type: str, args):
    try:
        hook_path = f'./.barb/{hook_type}'

        for arg in args:
            hook_path += str(arg)

        subprocess.run(['bash', hook_path])
    except Exception as e:
        print(f'An exception occurred when attempting to execute the git hook {hook_type}.')
        print(e)
        sys.exit(1)


def _execute_python_hook(hook_type: str):
    spec = importlib.util.spec_from_file_location(hook_type, f"./.barb/{hook_type}.py")
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)

    if not hasattr(foo, 'hook'):
        print('Invalid python git hook. Must have "hook" function to run.')

    try:
        res = foo.hook()

        if res is not None and not res:
            print(f"Failure indicated by hook function in {hook_type}.py via return value. Aborting.")
            sys.exit(1)

    except Exception as e:
        print(f"Exception encountered in hook {hook_type}.py. Aborting.")
        print(e)
        sys.exit(1)


def run_hook(params):
    hook = params[1]
    args = params[1:]

    hook_type = _get_py_hook_type(hook)

    if not hook_type:
        return

    if hook_type == 'SHELL':
        _execute_shell_hook(hook, args)
    elif hook_type == 'PYTHON':
        _execute_python_hook(hook)
