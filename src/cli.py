from .install import install_base_hooks
from .hooks import get_hook_names
from .run import run_hook
from .init import init
import argparse


def main():
    parser = argparse.ArgumentParser(prog='barb',
                                     description='Python Hooker')
    parser.add_argument('command', type=str, nargs='+')

    command = parser.parse_args().command
    if command[0] == 'init':
        init()

    elif command[0] == 'install':
        install_base_hooks()

    elif command[0] == 'run':
        if len(command) < 2:
            print('Must provide the name of the hook to run.')
            return

        if command[1] not in get_hook_names():
            print('Invalid git hook type.')
            return

        run_hook(command[1])
    else:
        print("Unrecognized ocommand.")


if __name__ == "__main__":
    # PYTHONPATH="`pwd`/." python3 setup.py install
    main()
