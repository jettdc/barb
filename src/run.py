import os.path
import subprocess
import importlib.util


def _get_py_hook_type(hook_type: str) -> None | str:
    if os.path.exists(f'./.barb/{hook_type}'):
        return 'SHELL'
    elif os.path.exists(f'./.barb/{hook_type}.py'):
        return 'PYTHON'
    else:
        return None


def _execute_shell_hook(hook_type: str):
    subprocess.run(['bash', f'./.barb/{hook_type}'])


def _execute_python_hook(hook_type: str):
    spec = importlib.util.spec_from_file_location(hook_type, f"./.barb/{hook_type}.py")
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)

    if hasattr(foo, 'hook'):
        foo.hook()
    else:
        print('Invalid python git hook. Must have "hook" function to run.')


def run_hook(hook: str):
    hook_type = _get_py_hook_type(hook)
    if not hook_type:
        return

    if hook_type == 'SHELL':
        _execute_shell_hook(hook)
    elif hook_type == 'PYTHON':
        _execute_python_hook(hook)
