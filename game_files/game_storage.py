""" storage for volatile game state """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from os import makedirs

from os.path import abspath
from os.path import join
from os.path import isfile

from typing import Callable

from jsons import dumps
from jsons import loads

from utils.singleton import Singleton

from rooms.exchange import Exchange

class GameStorage(metaclass=Singleton):
    """ ... """

    def __init__(self):
        """ ... """

        self._volatile_data = {}
        self._output = Exchange.output
        self._clients = {}

    def store_value(self, section: str, name: str, value: str) -> None:
        """ ... """

        data = self._volatile_data.setdefault(section, {})
        data[name] = value

    def load_value(self, section: str, name: str, default: str) -> str:
        """ ... """

        data = self._volatile_data.setdefault(section, {})
        return data.setdefault(name, default)

    def save(self, number: int):
        """ ... """

        for key, value in self._clients.items():
            save_function = value['save']
            save_function()

        full = join(abspath("."), "auto")
        makedirs(full, exist_ok=True)
        file = join(full, f'save_{number}.txt')

        with open(file=file, mode='wt', encoding='utf-8') as stream:
            stream.write(dumps(self._volatile_data))

        self._output.append(f'Saved game to "{file}"')

    def load(self, number: int):
        """ ... """

        full = join(abspath("."), "auto")
        makedirs(full, exist_ok=True)
        file = join(full, f'save_{number}.txt')

        if isfile(file):
            with open(file=file, mode='rt', encoding='utf-8') as stream:
                self._volatile_data = loads(stream.read())
                self._output.append(f'Load game from "{file}"')

            for key, value in self._clients.items():
                load_function = value['load']
                load_function()
        else:
            self._output.append(f'File not found: "{file}"')

    def register(self, label: str, save: Callable, load: Callable):
        """ ... """

        self._clients[label] = {'save': save, 'load': load}
