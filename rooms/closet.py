""" the 'bed' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper


class Closet(Room):
    """ 'Closet' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'Closet'
        kwargs['inventory'] = {'vial'}
        kwargs['description'] = 'I am in a closet'
        super().__init__(kwargs)
        self.help_verbs.update({'EMP', })

    @with_helper
    def handle_command(self,
                       verb: str,
                       noun: str,
                       callback: Callable) -> bool:
        """ ... """

        match verb:
            case "ENT":
                match noun:
                    case "DOO":
                        callback('enter', 'workroom')
                        return True

            case "EMP":
                match noun:
                    case "VIA":
                        self.say('I emptied the VIAL')
                        self._game.place('TAB', 'closet', '5')
                        return True

            case "TAK":
                match noun:
                    case "TAB":
                        obj = self._game.object('TAB')
                        if obj.location == 'closet':
                            obj.location = 'player'
                            count = obj.state
                            self.say(f'I got {count} tablets')
                        else:
                            self.say('I see no tablets im the closet')

                        return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": 'workroom'
        }
