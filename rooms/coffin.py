""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper

from texts import TEXTS


class Coffin(Room):
    """ 'Coffin' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):

        """ ... """

        kwargs['name'] = 'coffin'
        kwargs['description'] = 'I am in a coffin'
        kwargs['inventory'] = set()
        super().__init__(kwargs)
        self.help_verbs.update({'CUT', 'WIT', 'KIL'})

    @with_helper
    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        game = self._game

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
                        game.place('BOL', 'coffin', 'cut')
                        return True

            case 'KIL':
                match noun:
                    case 'DRA':
                        if (game.has('STA') and
                                game.has('MAL') and
                                game.has('DRA', 'coffin')):
                            game.place('DRA', 'coffin', 'nailed')

                            self.say(TEXTS['WIN'])
                            game.location = 'home'
                            return True

            case 'CLO':
                match noun:
                    case 'COF':
                        self.say("I close the coffin")
                        self.say("... I should not have done that!")
                        self.say("...... I suffocated")
                        self.say("......... I lost the game")
                        callback('enter', 'lost')
                        return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "UP": 'crypt',
        }
