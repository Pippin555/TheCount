""" the 'dungeon' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Dungeon(Room):
    """ 'Dungeon' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'dungeon'
        kwargs['description'] = 'I am in a dungeon'
        kwargs['inventory'] = {'ring on the wall', 'pit'}
        super().__init__(kwargs)

        self.help_verbs.update({'UP', 'TIE', 'TO', 'CLI'})

    # the dungeon has no with_helper, this is a special case
    def handle_command(self,
                       verb: str,
                       noun: str | None,
                       callback: Callable):
        """ ... """

        game = self._game

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
                        self.say('Tie what')
                        return True

                    case 'SHE':
                        self.say('Tie sheet to what')
                        return True

            case "TO":
                match noun:
                    case '':
                        self.say('Tie sheet to what')
                        return True

                    case 'RIN':
                        self.say('The sheet is now tied to a ring')
                        game.place('SHE', 'dungeon', 'ring')
                        return True

                return True

            case "TAK" | "GET":
                match noun:
                    case '' | None:
                        action = 'Take' if noun == 'TAK' else 'GET'
                        self.say(f'{action} what?')
                        return True

                    case "SHE":
                        # player gets the sheet
                        if game.has('SHE', ''):
                            self.say('The sheet is lost')
                            return True

                        if game.has('SHE', 'player'):
                            self.say('I already have the sheet')

                        elif game.has('SHE', 'dungeon', 'ring'):
                            self.say('I untied the sheet')

                        elif game.has('SHE', 'dungeon'):
                            self.say('I got the sheet')

                        game.place('SHE', 'player')
                        # let the end of the sheet vanish
                        game.place('END', '')

                        return True

                    case 'END':
                        if game.has('SHE', ''):
                            self.say('The sheet is lost')
                            return True

                        self.say('taken the end of the sheet')
                        game.place('END', 'player')
                        return True

            case 'DRO':
                match noun:
                    case None:
                        self.say('Drop what?')
                        return True

                    case "SHE":
                        # dropping the sheet will reset the state machine
                        if game.has('SHE', 'player'):
                            if game.has('END', 'dungeon', 'ring'):
                                game.place('SHE', '')
                                game.place('END', '')
                                self.say('You lost the sheet in the pit')
                                return True

                            game.place('SHE', 'dungeon')
                            self.say('I dropped the sheet')

                        elif game.has('SHE', 'dungeon', 'ring'):
                            self.say('I untied the sheet and dropped it')
                            game.place('SHE', 'dungeon')

                        game.place('END', '')
                        return True

                    case 'END':
                        if not game.has('END'):
                            self.say('I do not hold the end of the sheet')
                            return True

                        self.say('The end of the sheet is dropped in the pit')
                        self._game.place('END', 'dungeon', 'ring')
                        return True

            case 'CLI':
                match noun:
                    case None:
                        self.say('Climb what?')
                        return True

                    case 'SHE':
                        if self._game.has('END', 'dungeon', 'ring'):
                            return callback('enter', 'pit')

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "UP": "workroom",
        }