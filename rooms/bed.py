""" the 'bed' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Bed(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'Bed'
        kwargs['inventory'] = {'bed', 'pillow'}
        kwargs['description'] = 'I am lying in a large brass bed'
        super().__init__(kwargs)

        self.help_verbs = ['GET', 'HEL', 'LOO', 'SAV',
                           'DRO', 'CLI', 'INV', 'AUT',
                           'QUI', 'RES']

    def handle_command(self,
                       verb: str,
                       noun: str,
                       callback: Callable) -> bool:
        """ ... """

        if verb == 'GET' and noun == 'UP':
            return callback(verb='enter', noun='bedroom')

        if verb == 'HEL':
            self.say(self.format_help(self.help_verbs))
            return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "GET UP": None
        }
