""" base class for all 'rooms' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from abc import ABC, abstractmethod

from rooms.exchange import Exchange

from data import OBJECTS


class Room(ABC):
    """ ... """

    def __init__(self):
        """ ... """

        self._output = Exchange.output
        self._description = 'room'
        self._inventory = set()
        self._rooms = [self.name]

    def say(self, text: str):
        """ ... """

        self._output.append(text)

    @property
    @abstractmethod
    def name(self) -> str:
        """ ... """

        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """ ... """

        ...

    @property
    def inventory(self) -> set:
        """ ... """

        # the fixed inventory
        result = self._inventory
        # and the volatile inventory
        for key, obj in OBJECTS.items():
            if obj['location'] in self._rooms:
                result.add(obj['name'])

        return result

    @abstractmethod
    def handle_command(self, verb: str, noun: str) -> bool:
        """ ... """

        ...

    @property
    @abstractmethod
    def exits(self) -> dict:
        """ ... """

        ...
