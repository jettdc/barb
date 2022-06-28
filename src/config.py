from dataclasses import dataclass
import toml
from typing import Dict, Union, List
import platform


@dataclass
class BarbConfig:
    current_os: str
    current_os_family: str
    os_lock: str
    windows_interpreter: str
    interpreter_args: List[str]


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
            windows_interpreter=self._get_windows_interpreter(),
            interpreter_args=self._get_interpreter_args(),
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

# if __name__ == "__main__":
# load_config()
