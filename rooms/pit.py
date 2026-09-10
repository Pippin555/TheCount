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

        match verb:
            case 'CLI':
                match noun:
                    case None:
                        self.say('Climb what?')
                        return True

                    case 'SHE':
                        return callback('enter', 'dungeon')

            case 'LIG':
                match noun:
                    case 'MAT':
                        self.say('I lit a match')
                        if self._game.has('TOR', ''):
                            self._game.place('TOR', self.name)
                            self.say('I found a TORCH!')
                            return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "CLIMB": None
        }

