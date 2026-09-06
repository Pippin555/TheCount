""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Flowerbed(Room):
    """ 'FlowerBed' below the 'Bedroom window' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'flowerbed'
        kwargs['description'] = 'I am on a flowerbed'
        kwargs['inventory'] = set()
        super().__init__(kwargs)

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        if verb == 'CLI' and noun == 'SHE':
            return callback(verb='enter', noun='bedroom window')

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": "Dracula's bedroom"
        }
