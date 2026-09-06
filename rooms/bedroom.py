""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Bedroom(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'bedroom'
        kwargs['description'] = 'I am in a bedroom'
        kwargs['inventory'] = {'bed', 'window'}
        super().__init__(kwargs)

        self.tie_sheet = False
        self.sheet_tied = False

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        match verb:
            case 'GO':
                match noun:
                    case 'WIN':
                        return callback(verb='enter', noun='bedroom window')
                    case 'BED':
                        return callback(verb='enter', noun='bed')
            case "TIE":
                match noun:
                    case '':
                        self.say('tie what')
                        return True

                    case 'SHE':
                        self.tie_sheet = True
                        self.say('tie sheet to what')
                        return True
            case "TO":
                if self.tie_sheet:
                    match noun:
                        case '':
                            self.say('tie sheet to what')
                            return True
                        case 'BED':
                            self.say('The sheet is now tied to the bed')
                            self.sheet_tied = True
                            self._game.drop_inventory('SHE')
                            return True
                else:
                    self.say('tie what')

            case "TAK":
                if self.sheet_tied:
                    match noun:
                        case '':
                            self.say('take what')
                            return True
                        case 'END':
                            self.say('taken the end of the sheet')
                            self._game.get_inventory('END')
                            return True

            case "GET" | "TAK":
                if noun == "SHE":
                    self.tie_sheet = False
                    self.sheet_tied = False
                    self.say('untied the sheet')

                    # let the end of the sheet vanish
                    for obj in self._game.objects:
                        if obj.key == 'END':
                            obj.location = ''

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "NOR": "hall",
            "BED": "bed"
        }
