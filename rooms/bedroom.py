""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from enum import Enum
from enum import auto

from rooms.room import Room

from game_files.game_storage import GameStorage


class Bedroom(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'bedroom'
        kwargs['description'] = 'I am in a bedroom'
        kwargs['inventory'] = {'bed', 'window'}
        super().__init__(kwargs)
        self.help_verbs = ['GO', 'HEL', 'TIE', 'TO', 'AUT',
                           'TAK', 'GET', 'DRO', 'LOO', 'SAV',
                           'LOA', 'QUI', 'RES']
        self._window_open = False

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        match verb:
            case 'HEL':
                self.say(self.format_help(self.help_verbs))
                return True

            case 'OPE':
                match noun:
                    case 'WIN':
                        self.say('I opened the window')
                        self._window_open = True
                        return True

            case 'GO' | "ENT":
                match noun:
                    case 'WIN':
                        if self._window_open:
                            return callback(verb='enter', noun='bedroom window')
                        else:
                            self.say("I can't enter a closed window")
                            return True

                    case 'BED':
                        return callback(verb='enter', noun='bed')

            case "TIE":
                match noun:
                    case '' | None:
                        self.say('tie what')
                        return True

                    case 'SHE':
                        self.say('tie sheet to what')
                        return True

            case "TO":
                match noun:
                    case '':
                        self.say('tie sheet to what')
                        return True

                    case 'BED':
                        self.say('The sheet is now tied to the bed')
                        self._game.place('SHE', 'tied bed')
                        return True

                return True

            case "TAK" | "GET":
                match noun:
                    case '' | None:
                        self.say('take what')
                        return True

                    case "SHE":
                        # player gets the sheet
                        self._game.place('SHE', 'player')
                        self.say('You untied the sheet')

                        # let the end of the sheet vanish
                        self._game.place('END', '')
                        return True

                    case 'END':
                        self.say('taken the end of the sheet')
                        self._game.place('END', 'player')
                        return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "NOR": "hall",
            "BED": "bed"
        }
