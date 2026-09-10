""" base class for all 'rooms' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from abc import ABC, abstractmethod

from typing import Callable
from typing import TYPE_CHECKING
from functools import wraps

from utils.string_builder import StringBuilder

if TYPE_CHECKING:
    pass


def with_helper(func):
    @wraps(func)
    def wrapper(self, verb, noun, callback):
        if self.helper(verb=verb, noun=noun):
            return True
        return func(self, verb, noun, callback)

    return wrapper


class Room(ABC):
    """ ... """

    def __init__(self, kwargs: dict):
        """ ... """

        # required arguments
        self._game = kwargs['game']
        self._output = kwargs['output']
        self._description = kwargs['description']
        self._name = kwargs['name']

        # optional argument
        self._inventory = kwargs.get('inventory', set())

        self.help_verbs = {'GET', 'HEL', 'LOO', 'DRO', 'INV',
                           'RES', 'TAK', 'GO', 'WAI'}

    def say(self, text: str):
        """ ... """

        self._output.append(text)

    @property
    def name(self) -> str:
        """ ... """

        return self._name

    @property
    def description(self) -> str:
        """ ... """

        return self._description

    @property
    def inventory(self) -> set:
        """ the current inventory, both fixed and volatile """

        objs = {obj.name for obj in self._game.objects if obj.location == self.name}
        return objs | self._inventory

    @abstractmethod
    def handle_command(self,
                       verb: str,
                       noun: str,
                       callback: Callable) -> bool:
        """ ... """

        ...

    @property
    @abstractmethod
    def exits(self) -> dict:
        """ ... """

        ...

    def helper(self, verb: str, noun: str):
        """ ... """

        match verb:
            case 'HEL':
                self.say(self.format_help(self.help_verbs))
                return True

        return False

    def format_help(self, verbs: list[str]) -> str:
        """ ... """

        bld, aln = StringBuilder.bld_aln()
        app = bld.append

        aln(f'Help on the verbs of {self.name}:')
        for idx, verb in enumerate(sorted(verbs), 1):
            app(f'{verb:3} ')
            if idx % 8 == 0:
                aln('')

        if len(verbs) % 8 != 0:
            app('\n')

        return str(bld)
