""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper


class Bedroom(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'bedroom'
        kwargs['description'] = 'I am in a bedroom'
        kwargs['inventory'] = {'bed', 'window'}
        super().__init__(kwargs)
        self.help_verbs.update({'TIE', 'TO', 'OPE', 'ENT'})
        self._window_open = False

    @with_helper
    def handle_command(self,
                       verb: str,
                       noun: str | None,
                       callback: Callable):
        """ ... """

        game = self._game

        match verb:
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
                        if game.has('SHE', 'player'):
                            self.say('tie sheet to what')
                        else:
                            self.say('I do not have a sheet')
                        return True

            case "TO":
                match noun:
                    case '' | None:
                        if game.has('SHE', 'player'):
                            self.say('tie sheet to what')
                        else:
                            self.say('I do not have a sheet')
                        return True

                    case 'BED':
                        if game.has('SHE', 'player'):
                            self.say('The sheet is now tied to the bed')
                            self._game.place('SHE', 'bed', 'tied')
                        else:
                            self.say('I do not have a sheet')
                        return True

                return True

            case "TAK" | "GET":
                match noun:
                    case '' | None:
                        self.say('take what')
                        return True

                    case "SHE":
                        # player gets the sheet
                        if game.has('SHE', 'bed', 'tied'):
                            self.say('I untied the sheet')
                            game.place('SHE', 'player')
                        elif game.has('SHE', 'bedroom', ''):
                            self.say('I got the sheet')
                            game.place('SHE', 'player', '')

                        # let the end of the sheet vanish
                        self._game.place('END', '')
                        self.say("You can use the sheet on both ends to continue\ntry 'HELP'")
                        return True

                    case 'END':
                        if game.has('SHE', 'bed', 'tied'):
                            self.say('taken the end of the sheet')
                            self._game.place('END', 'player')
                        else:
                            self.say("I already have the sheet")
                        return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "NOR": "hall",
            "BED": "bed"
        }
