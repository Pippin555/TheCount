""" the 'dumb-waiter', pantry level, as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from _collections import deque

from rooms.room import Room


class DumbwaiterPantry(Room):
    """ 'Dumb-waiter' raised to the pantry level as 'room' in the game 'The Count' """

    def __init__(self):
        """ ... """

        super().__init__()

    @property
    def name(self):
        """ ... """

        return "dumbwaiter_pantry"

    @property
    def description(self):
        """ ... """

        return "I'm in the dumb-waiter, raised to the pantry level"

    @property
    def inventory(self):
        """ ... """

        return set()

    def handle_command(self, verb:str, noun: str):
        """ ... """

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "EAS": "pantry",
            "LOWER": "dumbwaiter_kitchen",
        }
