""" the 'bed' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from collections import deque

from typing import TYPE_CHECKING

from rooms.room import Room

if TYPE_CHECKING:
    from game_handlers import GameState

from utils.command_router import CommandRouter


class Bed(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self,
                 game: GameState,
                 output: deque[str]):
        """ ... """

        inventory = {'bed', 'pillow'}
        super().__init__(game=game,
                         name='bed',
                         output=output,
                         inventory=inventory)

    @property
    def description(self) -> str:
        """ ... """

        return "I am lying in a bed"

    def handle_command(self, verb: str, noun: str) -> bool:
        """ ... """

        if verb == 'GET' and noun == 'UP':
            CommandRouter().handle('enter', 'bedroom')
            return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "GET UP": None
        }
