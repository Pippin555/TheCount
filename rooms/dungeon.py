""" the 'dungeon' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable
from enum import Enum
from enum import auto

from rooms.room import Room

from game_files.game_storage import GameStorage


class DungeonState(Enum):
    """ ... """

    START = auto()
    TIE_WHAT = auto()
    TO_WHAT = auto()
    SHEET_TIED = auto()
    TAKE_WHAT = auto()
    TAKE_END = auto()
    DROP_WHAT = auto()
    END_DROPPED = auto()

class Dungeon(Room):
    """ 'Dungeon' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'dungeon'
        kwargs['description'] = 'I am in a dungeon'
        kwargs['inventory'] = {'rings on the wall', 'pit'}
        super().__init__(kwargs)

        self.help_verbs = ['UP', 'GO', 'HEL', 'TIE', 'TO',
                           'TAK', 'GET', 'DRO', 'CLI', 'I',
                           'LOO', 'SAV', 'AUT', 'QUI', 'RES'
                           ]
        self.state = DungeonState.START

        GameStorage().register(label=self.name,
                               save=self.save,
                               load=self.load)

    def load(self) -> None:
        """ ... """

        default = DungeonState.START.name
        value = GameStorage().load_value(section=self.name,
                                         name='state',
                                         default=default)
        self.state = DungeonState[value]

    def save(self):
        """ ... """

        GameStorage().store_value(section=self.name,
                                  name='state',
                                  value=self.state.name)
        ...

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        have_sheet = False
        have_end = False

        for obj in self._game.objects:
            if obj.location == 'player':
                if obj.key == 'SHE':
                    have_sheet = True
                if obj.key == 'END':
                    have_end = True

        match verb:
            case 'UP':
                return callback('enter', 'workroom')

            case 'GO':
                if noun == 'UP':
                    return callback('enter', 'workroom')

            case 'HEL':
                if noun == 'PIT':
                    self.say("Remember the bed")
                else:
                    self.say(self.format_help(self.help_verbs))
                    self.say("Problem with the pit?, try HELP PIT")

                return True

            case "TIE":
                if self.state == DungeonState.START:
                    if noun == "SHE":
                        if not have_sheet:
                            self.say("I have no sheet")
                            return False
                        self.say("To what?")
                        self.state = DungeonState.TO_WHAT
                        return True
                    else:
                        self.say('Tie what?')
                    return True

                return False

            case "TO":
                if self.state == DungeonState.TO_WHAT:
                    if not have_sheet:
                        return False

                    if noun == "RIN":
                        self.say('The sheet is tied to one of the rings')
                        self.state = DungeonState.TAKE_END
                    return True

                return False

            case 'TAK' | 'GET':
                if self.state == DungeonState.TAKE_END:
                    if not have_sheet:
                        return False

                    if noun == "END":
                        self.say('I have the end of the sheet')
                        for obj in self._game.objects:
                            if obj.key == 'END':
                                obj.location = 'player'

                        self.state = DungeonState.DROP_WHAT

                    return True

            case 'DRO':
                if noun == "SHE":
                    # dropping the sheet will reset the state machine
                    self.say('You untied the sheet and dropped it')
                    for obj in self._game.objects:
                        if obj.key == 'SHE':
                            obj.location = self.name
                            break
                    return True

                if self.state == DungeonState.DROP_WHAT:
                    if not have_sheet or not have_end:
                        self.say('I do not hold the end of the sheet')
                        return False

                    if noun == 'END':
                        self.say('The end of the sheet is dropped in the pit')
                        self.state = DungeonState.END_DROPPED
                        for obj in self._game.objects:
                            if obj.key == 'END':
                                obj.location = ''

                    return True

            case 'TAK':
                if noun == 'SHE':
                    self.state = DungeonState.START
                    for obj in self._game.objects:
                        if obj.key == 'SHE':
                            obj.location = 'player'
                        elif obj.key == 'END':
                            obj.location = ''

            case 'CLI':
                if self.state == DungeonState.END_DROPPED:
                    if not have_sheet:
                        return False

                    if noun == 'SHE':
                        return callback('enter', 'pit')

                    return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "UP": "dungeon",
        }
