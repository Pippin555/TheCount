""" the 'dumb-waiter', workroom level, as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper


class DumbwaiterWorkroom(Room):
    """ 'Dumbwaiter at the workroom level as 'room' in the game 'The Count' """


    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'dumbwaiter workroom'
        kwargs['description'] = "I'm in a dumb-waiter, lowered to the workroom level"
        kwargs['inventory'] = set()
        super().__init__(kwargs)
        self.help_verbs.update({'ENT', 'RAI'})

    @with_helper
    def handle_command(self,
                       verb: str,
                       noun: str | None,
                       callback: Callable):
        """ ... """

        match verb:
            case 'ENT':
                match noun:
                    case None:
                        self.say('Enter what?')
                        return True

                    case 'ROO':
                        callback('enter', 'workroom')
                        return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "EAS": "workroom",
            "RAI": "dumbwaiter kitchen",
        }
