import sys
from dataclasses import dataclass
import toml
from typing import Dict, Union, List
import platform
from jettools import dict_tools

@dataclass
class InterpreterConfig:
    ext: str
    cmd: str
    args : List[str]

@dataclass
class BarbConfig:
    current_os: str
    current_os_family: str
    os_lock: str
    default_interpreter: InterpreterConfig
    interpreters: List[InterpreterConfig]


class BarbConfigurationException(Exception):
    pass


class Config:
    _instance: 'Config' = None

    def __init__(self):
        try:
            with open('./.barbrc.toml', 'r') as f:
                self.loaded = toml.loads(f.read())
        except Exception as e:
            raise BarbConfigurationException(
                'Failed to open configuration file. Ensure you have a file in the root of your project directory called .barbrc.toml')

        self.config = BarbConfig(
            current_os=self._get_current_os(),
            current_os_family=self._get_current_os_family(),
            os_lock=self._get_os_lock(),
            default_interpreter=self._get_default_interpreter(),
            interpreters=self._get_interpreters(),
        )

    @staticmethod
    def get_instance() -> 'Config':
        if Config._instance is None:
            Config._instance = Config()
        return Config._instance

    def _get_current_os(self):
        os = platform.system().lower()
        if os == 'windows' or os == 'linux' or os == 'darwin':
            return os
        else:
            raise Exception(f'Unsupported operating system: {os}')

    def _get_current_os_family(self):
        os = platform.system().lower()
        if os == 'windows':
            return os
        elif os == 'linux' or os == 'darwin':
            return 'unix'
        else:
            raise Exception(f'Unsupported operating system: {os}')

    def _get_os_lock(self) -> Union[str, None]:
        passed = self.loaded.get('os-lock')
        ok = ['windows', 'linux', 'darwin', 'unix', 'none']

        if passed is None or passed.lower() == 'none':
            return None

        if passed.lower() in ok:
            return passed.lower()

        raise BarbConfigurationException(f'os-lock config option not recognized. Choose from {str(ok)}')

    def os_lock_ok(self):
        if self.config.os_lock is None:
            return True

        elif self.config.os_lock == 'unix' and (self.config.current_os == 'linux' or self.config.current_os == 'darwin'):
            return True

        else:
            return self.config.os_lock == self.config.current_os

    def _get_default_interpreter(self):
        default_interpreter_config = dict_tools.get(self.loaded, ['os', self._get_current_os(), 'default'])
        if default_interpreter_config is None:
            return InterpreterConfig('default', 'bash', [])

        interpreter = default_interpreter_config.get('interpreter')
        if interpreter is None:
            raise BarbConfigurationException('Invalid config. Missing interpreter for default.')

        args = default_interpreter_config.get('args')
        if args is not None and not isinstance(args, list):
            raise BarbConfigurationException('Invalid config. Interpreter args must be a list.')
        elif args is None:
            args = []

        return InterpreterConfig('default', interpreter, args)

    def _get_interpreters(self) -> List[InterpreterConfig]:
        interpreters = []

        other_interpreters = dict_tools.get(self.loaded, ['os', self._get_current_os()])
        if other_interpreters is None or not isinstance(other_interpreters, dict):
            return []

        for k, v in other_interpreters.items():
            if k == 'default':
                continue

            interpreter = v.get('interpreter')
            if interpreter is None:
                raise BarbConfigurationException('Invalid config. Missing interpreter for default.')

            args = v.get('args')
            if args is not None and not isinstance(args, list):
                raise BarbConfigurationException('Invalid config. Interpreter args must be a list.')
            elif args is None:
                args = []

            interpreters.append(InterpreterConfig(k, interpreter, args))
        return interpreters

    def _get_windows_interpreter(self) -> Union[str, None]:
        arg = self.loaded.get('windows-interpreter')

        if arg is None:
            return 'bash'

        return arg

    def _get_interpreter_args(self) -> List[str]:
        arg = self.loaded.get('interpreter-args')

        if arg is None:
            return []

        if not isinstance(arg, list):
            raise BarbConfigurationException('Invalid interpreter args. Must be a list.')

        return arg

if __name__ == "__main__":
    # sys.path.append('../')
    print(Config.get_instance().config)
