""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room

from texts import TEXTS


class Coffin(Room):
    """ 'Coffin' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):

        """ ... """

        kwargs['name'] = 'coffin'
        kwargs['description'] = 'I am in a coffin'
        kwargs['inventory'] = set()
        super().__init__(kwargs)

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        match verb:
            case 'CUT':
                match noun:
                    case 'BOL':
                        self.say('With what?')
                        return True

                    case _:
                        self.say('Cut what?')
                        return True

            case 'WIT':
                match noun:
                    case 'FIL':
                        self.say('The bolt is cut')
                        self._game.place('BOL', 'coffin cut')
                        return True

            case 'KIL':
                match noun:
                    case 'DRA':
                        if self._game.has('STA') and \
                            self._game.has('MAL') and \
                            self._game.has('DRA', 'coffin'):

                            self.say(TEXTS['WIN'])
                            return True
        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "UP": 'crypt',
        }
