""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from rooms.room import Room

from utils.command_router import CommandRouter


class Kitchen(Room):
    """ 'Kitchen' as 'room' in the game 'The Count' """

    def __init__(self):
        """ ... """

        super().__init__()

    @property
    def name(self):
        """ ... """

        return "kitchen"

    @property
    def description(self):
        """ ... """

        return "I'm in a kitchen, I see a dumb-waiter"

    def handle_command(self, verb:str, noun: str):
        """ ... """

        if verb == "GO" and noun == "DUM":
            CommandRouter().handle('enter', 'dumbwaiter_kitchen')
            return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": "dumbwaiter_kitchen",
            "EAS": "hall",
        }
