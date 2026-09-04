""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from _collections import deque

from rooms.room import Room

from data import OBJECTS


class Bedroom(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self):
        """ ... """

        super().__init__()

    @property
    def name(self):
        """ ... """

        return "bedroom"

    @property
    def description(self):
        """ ... """

        return "I'm in the bedroom"

    @property
    def inventory(self):
        """ ... """

        result = set()
        for obj in OBJECTS:
            if obj['location'] == 'bedroom':
                result.add(obj['name'])
        return result

    def handle_command(self, verb:str, noun: str):
        """ ... """

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "NOR": "hall"
        }
