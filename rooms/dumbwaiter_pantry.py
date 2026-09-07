""" the 'dumb-waiter', pantry level, as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from _collections import deque

from rooms.room import Room


class DumbwaiterPantry(Room):
    """ 'Dumb-waiter' raised to the pantry level as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'dumbwaiter pantry'
        kwargs['description'] = "I'm in a dumb-waiter, raised to the pantry level"
        kwargs['inventory'] = set()
        super().__init__(kwargs)

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "EAS": "pantry",
            "LOW": "dumbwaiter kitchen",
        }
