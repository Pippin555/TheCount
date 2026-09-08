""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Oven(Room):
    """ 'Hall'Oven' a 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):

        """ ... """

        kwargs['name'] = 'oven'
        kwargs['description'] = 'I am in a huge solar oven'
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
            "WES": "kitchen",
        }
