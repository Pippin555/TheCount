""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from _collections import deque

from rooms.room import Room


class Hall(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self, output: deque):
        """ ... """

        super().__init__(output=output)

    @property
    def name(self):
        """ ... """

        return "hall"

    @property
    def description(self):
        """ ... """

        return "I'm in a hall"

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
            "SOU": "bedroom",
            "NOR": "bathroom",
            "WES": "kitchen",
            "EAS": "courtyard",
        }
