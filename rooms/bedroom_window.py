""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper

class BedroomWindow(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'window ledge'
        kwargs['description'] = 'I am on the window ledge'
        kwargs['inventory'] = set()
        super().__init__(kwargs)
        self.help_verbs.update({'CLI', })

    @with_helper
    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        match verb:
            case 'DRO':
                if noun == 'END':
                    if self._game.has('END'):
                        self.say('I dropped the end of the sheet over the ledge of the window')
                        self._game.place('END', 'bed', 'tied')
                        return True

            case 'CLI':
                if noun == 'SHE' and \
                    self._game.has('SHE', 'bed', 'tied') and \
                    self._game.has('END', 'bed', 'tied'):
                    callback(verb='enter', noun='flowerbed')
                else:
                    self.say(f"I can't {verb} {noun}")

                return True

            case 'ENT':
                match noun:
                    case 'WIN':
                        return callback(verb='enter', noun='bedroom')

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": "bedroom"
        }
