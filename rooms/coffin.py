""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Coffin(Room):
    """ 'Coffin' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):

        """ ... """

        kwargs['name'] = 'coffin'
        kwargs['description'] = 'I am in a coffin'
        kwargs['inventory'] = {'bolt', }
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
                        self._inventory= {'bolt cut', }
                        return True

            # case 'GO':
            #     match noun:
            #         case 'UP':
            #             return callback('enter', 'crypt')
        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "UP": 'crypt',
        }
