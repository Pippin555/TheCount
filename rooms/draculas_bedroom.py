""" the 'bed' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class DraculasBedroom(Room):
    """ 'Pantry' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = "Dracula's bedroom"
        kwargs['inventory'] = {"Painting", }
        kwargs['description'] = "I am in Dracula's bedroom"
        super().__init__(kwargs)
        self.painting = 'hanging'

    def handle_command(self,
                       verb: str,
                       noun: str,
                       callback: Callable) -> bool:
        """ ... """

        if verb == 'REM' and noun == 'PAI':
            if self.painting == 'hanging':
                self.painting = 'removed'
                for obj in self._game.objects:
                    if obj.key == 'STA':
                        obj.location = self.name
                        return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": 'flowerbed'
        }
