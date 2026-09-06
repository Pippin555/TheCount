""" base class for all 'rooms' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from abc import ABC, abstractmethod

from collections import deque

from typing import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_state import GameState


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
