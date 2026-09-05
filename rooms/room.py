""" base class for all 'rooms' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from abc import ABC, abstractmethod

from rooms.exchange import Exchange

from data import OBJECTS


class Room(ABC):
    """ ... """

    def __init__(self, name: str, inventory: set | None = None):
        """ ... """

        self._output = Exchange.output
        self._description = 'room'
        self._inventory = inventory if inventory is not None else set()
        self._name = name

    def say(self, text: str):
        """ ... """

        self._output.append(text)

    @property
    def name(self) -> str:
        """ ... """

        return self._name

    @property
    @abstractmethod
    def description(self) -> str:
        """ ... """

        ...

    @property
    def inventory(self) -> set:
        """ ... """

        objs = {obj.name for obj in OBJECTS if obj.location == self.name}
        return objs | self._inventory

    @abstractmethod
    def handle_command(self, verb: str, noun: str) -> bool:
        """ ... """

        ...

    @property
    @abstractmethod
    def exits(self) -> dict:
        """ ... """

        ...
