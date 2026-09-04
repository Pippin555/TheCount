""" the 'dumb-waiter', kitchen level, as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from rooms.room import Room


class DumbwaiterKitchen(Room):
    """ 'Kitchen' as 'room' in the game 'The Count' """

    def __init__(self):
        """ ... """

        super().__init__()

    @property
    def name(self):
        """ ... """

        return "dumbwaiter_kitchen"

    @property
    def description(self):
        """ ... """

        return "I'm in the dumb-waiter, at the kitchen level"

    @property
    def inventory(self):
        """ ... """

        return set()

    def handle_command(self, verb:str, noun: str):
        """ ... """

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "RAISE": "dumbwaiter_pantry",
            "EAS": "kitchen",
            "LOWER": "dumbwaiter_workroom",
        }
