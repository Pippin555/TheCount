""" the 'bed' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper


class Bed(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'bed'
        kwargs['inventory'] = {'pillow'}
        kwargs['description'] = 'I am lying in a large brass bed'
        super().__init__(kwargs)
        self.help_verbs.update({'AUT',})

    @with_helper
    def handle_command(self,
                       verb: str,
                       noun: str,
                       callback: Callable) -> bool:
        """ ... """

        game = self._game

        match verb:
            case 'GET':
                match noun:
                    case 'UP':
                        return callback(verb='enter', noun='bedroom')

            case 'DRO':
                match noun:
                    case 'SHE':
                        if game.has('SHE', 'player'):
                            if game.has('TOR', 'player', 'lit'):
                                self.say('The sheet burned, you are now stuck')
                                self.say("\ntry 'RESTART' to play again")
                            else:
                                game.place('SHE', 'bed', '')
                        else:
                            self.say('I have no sheet')
        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "GET UP": None
        }
