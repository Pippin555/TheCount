""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper


class Pit(Room):
    """ 'Hall' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):

        """ ... """

        kwargs['name'] = 'pit'
        kwargs['description'] = 'I am in a very dark pit'
        kwargs['inventory'] = set()
        super().__init__(kwargs)

        self.help_verbs.update({'CLI', 'LIG'})

    @with_helper
    def handle_command(self,
                       verb:str,
                       noun: str| None,
                       callback: Callable):
        """ ... """

        game = self._game

        match verb:
            case 'CLI':
                match noun:
                    case None:
                        self.say('Climb what?')
                        return True

                    case 'SHE':
                        if game.has('TOR', 'player', 'lit'):
                            if not game.has('SHE', ''):
                                game.place('SHE', '')
                                game.place('END', '')
                                self.say('The sheet burned, you are now stuck')
                            else:
                                self.say('There is no sheet anymore, you are now stuck')
                            self.say("\nTry to 'RESTART'")
                            return True

                        else:
                            return callback('enter', 'dungeon')

            case 'LIG':
                match noun:
                    case 'MAT':
                        self.say('I lit a match')
                        if game.has('TOR', ''):
                            game.place('TOR', 'pit', '')
                            self.say('I found a TORCH!')
                            return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "CLIMB": None
        }

