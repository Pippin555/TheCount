""" the 'gate' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Gate(Room):
    """ 'Hall' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):

        """ ... """

        kwargs['name'] = 'gate'
        kwargs['description'] = 'I am outside the gate of the Castle'
        kwargs['inventory'] = {'Angry townspeople', }
        super().__init__(kwargs)
        self._yelled = False

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        if not self._yelled:
            self._output.append('Angry townspeople throw stones at me')
            self._output.append('They yell that I was supposed to kill Dracula!')
        return True

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": "courtyard",
        }
