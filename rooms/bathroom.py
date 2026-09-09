""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Bathroom(Room):
    """ 'Hall' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):

        """ ... """

        kwargs['name'] = 'Bathroom'
        kwargs['description'] = 'I am in a bathroom'
        kwargs['inventory'] = {'Mirror', }
        super().__init__(kwargs)

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        match verb:
            case 'LOO':
                match noun:
                    case 'MIR':
                        self.say("I see bitemarks and on my neck and I feel drained.")
                        self.say("I hope I can complete this adventure.")
                        return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "SOU": "hall",
        }
