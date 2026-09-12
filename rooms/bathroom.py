""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper


class Bathroom(Room):
    """ 'Hall' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):

        """ ... """

        kwargs['name'] = 'bathroom'
        kwargs['description'] = 'I am in a bathroom'
        kwargs['inventory'] = set()
        super().__init__(kwargs)

    @with_helper
    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        game = self._game

        match verb:
            case 'LOO':
                match noun:
                    case 'MIR':
                        if (game.has('MIR', 'bathroom', '') |
                                game.has('MIR', 'player')):

                            match self._game.day:
                                case 1:
                                    self.say('I look healthy today')
                                    return True

                                case _:
                                    self.say("I see bitemarks and on my neck and I feel drained.")
                                    self.say("I hope I can complete this adventure.")
                                    return True

                        else:
                            self.say('There is no mirror in the bathroom.')
                            return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "SOU": "hall",
        }
