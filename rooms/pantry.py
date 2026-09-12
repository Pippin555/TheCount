""" the 'bed' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper

class Pantry(Room):
    """ 'Pantry' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'pantry'
        kwargs['inventory'] = set()
        kwargs['description'] = 'I am in a pantry'
        super().__init__(kwargs)

    @with_helper
    def handle_command(self,
                       verb: str,
                       noun: str| None,
                       callback: Callable) -> bool:
        """ ... """

        match verb:
            case 'ENT':
                match noun:
                    case 'DUM':
                        callback('enter', 'dumbwaiter pantry')
                    case _:
                        self.say('Enter what?')

                return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": 'dumbwaiter pantry'
        }
