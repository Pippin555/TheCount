""" the 'dumb-waiter', workroom level, as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from _collections import deque

from rooms.room import Room


class DumbwaiterWorkroom(Room):
    """ 'Dumbwaiter at the workroom level as 'room' in the game 'The Count' """

    def __init__(self):
        """ ... """

        super().__init__()

    @property
    def name(self):
        """ ... """

        return "dumbwaiter_workroom"

    @property
    def description(self):
        """ ... """

        return "I'm in the dumb-waiter, lowered to the workroom level"

    def handle_command(self, verb:str, noun: str):
        """ ... """

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "EAS": "workroom",
            "RAISE": "dumbwaiter_kitchen",
        }
