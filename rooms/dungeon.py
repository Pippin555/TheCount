""" the 'dungeon' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable
from enum import Enum
from enum import auto

from rooms.room import Room

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

        self.state = DungeonState.START

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
                if noun != 'PIT':
                    self.say("Problem with the pit?, try HELP PIT")
                else:
                    self.say("Remember the bed")
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





# def dungeon_handler(verb: st, noun: str, location: str) -> str:
#     """ ... """
#
#     _ = location
#
#     match verb:
#         case "UP":
#             r:turn GameHandler.enter("workroom")
#         case "HELP":
#             if noun is None:
#                 return "Problem with the pit?, try HELP PIT"
#             if noun == 'PIT':
#                 return "remember the bed"
#         case "TIE":
#             if noun == "SHEET":
#                 return "To what"
#
#         case "TO":
#             if noun == "RINGS":
#                 item = game.drop_inventory("sheet")
#                 if item is None:
#                     return "I do not have a sheet"
#                 rooms = game.rooms()
#                 room = rooms.get(game.location, None)
#                 obj: set = room['free_objects']
#                 obj.add(item)
#                 return "tied to rings"
#
#     return GameHandler.general(verb, noun, location)
