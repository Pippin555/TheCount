""" the 'dungeon' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room

from data import VERBS
from data import NOUNS


class Dungeon(Room):
    """ 'Dungeon' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'dungeon'
        kwargs['description'] = 'I am in a dungeon'
        kwargs['inventory'] = {'rings on the wall', 'pit', 'vent'}
        super().__init__(kwargs)

        self.help_verbs = ['UP', 'GO', 'HEL', 'TIE', 'TO',
                           'TAK', 'GET', 'DRO', 'CLI', 'I',
                           'LOO', 'SAV', 'AUT', 'QUI', 'RES'
                           ]

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        match verb:
            case 'UP':
                return callback('enter', 'workroom')

            case 'HEL':
                if noun == 'PIT':
                    self.say("Remember the bed")
                else:
                    self.say(self.format_help(self.help_verbs))
                    self.say("Problem with the pit?, try HELP PIT")

                return True

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

                    case 'RIN':
                        self.say('The sheet is now tied to a ring')
                        self._game.place('SHE', 'tied ring')
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

            case 'DRO':
                match noun:
                    case "SHE":
                        # dropping the sheet will reset the state machine
                        self.say('You untied the sheet and dropped it')
                        self._game.place('SHE', self.name)
                        self._game.place('END', '')
                        return True

                    case 'END':
                        if not self._game.has('END'):
                            self.say('I do not hold the end of the sheet')
                            return False

                        self.say('The end of the sheet is dropped in the pit')
                        self._game.place('END', 'tied ring')

                        return True

            case 'CLI':
                if noun == 'SHE' and \
                    self._game.has('SHE', 'tied ring') and \
                    self._game.has('END', 'tied ring'):
                    return callback('enter', 'pit')
                else:
                    verb = VERBS.get(verb, verb)
                    noun = NOUNS.get(noun, noun)
                    self.say(f"I can't {verb} {noun}")
                    return False

                return True

            case "ENT":
                match noun:
                    case "VEN":
                        self.say('You’re not the size of bat')
                        return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "UP": "workroom",
        }