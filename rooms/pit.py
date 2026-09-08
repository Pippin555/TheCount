""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Pit(Room):
    """ 'Hall' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):

        """ ... """

        kwargs['name'] = 'pit'
        kwargs['description'] = 'I am in a very dark pit'
        kwargs['inventory'] = set()
        super().__init__(kwargs)

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        match verb:
            case 'CLI':
                if noun == 'SHE':
                    return callback('enter', 'dungeon')
                    return True

            case 'LIG':
                match noun:
                    case 'MAT':
                        self.say('You light a match')
                        if self._game.has('TOR', ''):
                            self._game.place('TOR', self.name)
                            self.say('You found a TORCH!')
                            return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "CLIMB": None
        }

