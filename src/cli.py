from .init import init
import argparse

def main():
    parser = argparse.ArgumentParser(prog='py-hook',
                                     description='Python Hooker')
    parser.add_argument('command', type=str)

    command = parser.parse_args().command

    if command == 'init':
        init()
    elif command == 'install':
        print('installing')
    else:
        print('Invalid command.')

if __name__ == "__main__":
    main()