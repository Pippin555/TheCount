""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class BedroomWindow(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'window ledge'
        kwargs['description'] = 'I am on the window ledge'
        kwargs['inventory'] = set()
        super().__init__(kwargs)

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        if verb == 'CLI' and noun == 'SHE':
            callback(verb='enter', noun='flowerbed')
            return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": "bedroom"
        }
