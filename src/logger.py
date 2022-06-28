from enum import Enum


class Color(Enum):
    Black = '\u001b[30m'
    Red = '\u001b[31m'
    Green = '\u001b[32m'
    Yellow = '\u001b[33m'
    Blue = '\u001b[34m'
    Magenta = '\u001b[35m'
    Cyan = '\u001b[36m'
    White = '\u001b[37m'
    Reset = '\u001b[0m'


class Logger:
    instance = None

    @staticmethod
    def get_logger():
        if Logger.instance is None:
            Logger.instance = Logger()
        return Logger.instance

    def info(self, *args):
        print("[barb]", *args)

    def error(self, *args, color=False):
        print(f"{Color.Red.value if color else ''}[barb] ERROR:", *args, end=f'{Color.Reset.value if color else ""}\n')
