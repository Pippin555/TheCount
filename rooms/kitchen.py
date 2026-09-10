""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Kitchen(Room):
    """ 'Kitchen' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'kitchen'
        kwargs['description'] = 'I am in a kitchen'
        kwargs['inventory'] = set()
        super().__init__(kwargs)

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        game = self._game

        match verb:
            case 'ENT' | 'GO':
                match noun:
                    case 'DUM':
                        return callback('enter', 'dumbwaiter kitchen')

                    case 'OVE':
                        # -1 daytime
                        #  0 sunset
                        # +1 night
                        if game.sunset == -1:
                            self.say('Solar oven is UNSAFE to enter in daytime')
                            return True
                        elif game.sunset == 1:
                            return callback('enter', 'oven')

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": "dumbwaiter kitchen",
            "EAS": "hall",
            "OVEN": None,
        }
