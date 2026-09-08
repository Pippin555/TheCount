""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Passage(Room):
    """ 'Hall' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):

        """ ... """

        kwargs['name'] = 'passage'
        kwargs['description'] = 'I am in a passage'
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
            "NOR": "crypt",
            "EAS": "dracula's bedroom",
        }
