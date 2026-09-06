""" the 'workroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Workroom(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'workroom'
        kwargs['description'] = 'I am in a workroom'
        kwargs['inventory'] = set()
        super().__init__(kwargs)

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        if verb == 'DOW':
            return callback('enter', 'dungeon')

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": "dumbwaiter workroom",
            "DOW": "dungeon",
        }
