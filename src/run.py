import os.path
import subprocess

def _py_hook_exists(hook_type: str) -> bool:
    return os.path.exists(f'./.py-hook/{hook_type}')

def _execute_hook(hook_type: str):
    subprocess.run(['bash', f'./.py-hook/{hook_type}'])

def run_hook(hook_type: str):
    if not _py_hook_exists(hook_type):
        return

    _execute_hook(hook_type)