""" the 'bed' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Closet(Room):
    """ 'Closet' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'Closet'
        kwargs['inventory'] = {'empty vial'}
        kwargs['description'] = 'I am in a closet'
        super().__init__(kwargs)

    def handle_command(self,
                       verb: str,
                       noun: str,
                       callback: Callable) -> bool:
        """ ... """

        match verb:
            case "ENT":
                match noun:
                    case "DOO":
                        callback('enter', 'workroom')
                        return True

            case "EMP":
                match noun:
                    case "VIA":
                        self.say('You emptied the VIAL')
                        return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": 'workroom'
        }
