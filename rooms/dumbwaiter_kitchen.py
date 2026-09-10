""" the 'dumb-waiter', kitchen level, as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper


class DumbwaiterKitchen(Room):
    """ 'Kitchen' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'dumbwaiter kitchen'
        kwargs['description'] = 'I am in a dumb-waiter at the kitchen level'
        kwargs['inventory'] = set()
        super().__init__(kwargs)
        self.help_verbs.update({'ENT', 'RAI', 'LOW'})

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
                        self.say("Enter what?")
                        return True

                    case 'ROO':
                        return callback('enter', 'kitchen')

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "RAI": "dumbwaiter pantry",
            "EAS": "kitchen",
            "LOW": "dumbwaiter workroom",
        }
