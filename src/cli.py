from src.install import install_base_hooks
from src.hooks import get_hook_names
from src.logger import Logger
from src.run import run_hook
from src.init import init
from src.ls import ls
import argparse


def main():
    log = Logger.get_logger()

    parser = argparse.ArgumentParser(prog='barb',
                                     description='Python Hooker')
    parser.add_argument('command', type=str, nargs='+')

    command = parser.parse_args().command

    if command[0] == 'init':
        if init():
            log.info("Successfully initialized & installed git hooks.")

    elif command[0] == 'install':
        if install_base_hooks():
            log.info("Successfully installed git hooks.")

    elif command[0] == 'ls' or command[0] == 'list':
        ls()

    elif command[0] == 'sanitize':
        # sanitize()
        log.info('Functionality not yet implemented.')
        return

    elif command[0] == 'run':
        if len(command) < 2:
            log.error('Must provide the name of the hook to run.')
            return

        if command[1] not in get_hook_names():
            log.error('Invalid git hook type.')
            return

        run_hook(command[1:])
    else:
        log.info("Unrecognized command. For a list of commands, type 'barb -h'")


if __name__ == "__main__":
    main()

    # Don't support interactive flag, doesn't work on windows
