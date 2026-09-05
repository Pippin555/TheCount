""" the 'bed' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from rooms.room import Room

from data import OBJECTS

from utils.command_router import CommandRouter


class Bed(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self):
        """ ... """

        super().__init__()

        self._inventory = {'bed', 'pillow' }
        self._rooms.append('bedroom')

    @property
    def name(self):
        """ ... """

        return "bed"

    @property
    def description(self) -> str:
        """ ... """

        return "I am lying in a bed"

    def handle_command(self, verb: str, noun: str) -> bool:
        """ ... """

        if verb == 'GET' and noun == 'UP':
            CommandRouter().handle('enter', 'bedroom')
            return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "GET UP": None
        }