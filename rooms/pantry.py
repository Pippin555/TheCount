""" the 'bed' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Pantry(Room):
    """ 'Pantry' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'Pantry'
        kwargs['inventory'] = {'matches', 'garlic'}
        kwargs['description'] = 'I am in a pantry'
        super().__init__(kwargs)

    def handle_command(self,
                       verb: str,
                       noun: str,
                       callback: Callable) -> bool:
        """ ... """

        # if verb == 'GET' and noun == 'UP':
        #     return callback(verb='enter', noun='bedroom')

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": 'dumbwaiter pantry'
        }
