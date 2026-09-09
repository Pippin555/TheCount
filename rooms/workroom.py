""" the 'workroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Workroom(Room):
    """ 'Bed' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'workroom'
        kwargs['description'] = 'I am in a workroom'
        kwargs['inventory'] = {'door', 'lock', 'vent'}
        super().__init__(kwargs)

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        match verb:
            case "ENT":
                match noun:
                    case "DUM":
                        return callback('enter', 'dumbwaiter workroom')

                    case "VEN":
                        self.say("A spooky voice is heard")
                        self.say('You’re not the size of bat')
                        return True

                    case "DOO":
                        return callback('enter', 'closet')

            case 'DOW':
                return callback('enter', 'dungeon')

            case "GO":
                match noun:
                    case "DOW":
                        return callback('enter', 'dungeon')

            case "PIC":
                match noun:
                    case "LOC":
                        self.say('You picked the lock of the door')
                        return True

            case 'OPE':
                match noun:
                    case "DOO":
                        self.say('You opened the door')
                        return True

            case 'CLO':
                match noun:
                    case "DOO":
                        self.say('You closed the door')
                        return True

            case 'LOC':
                match noun:
                    case "DOO":
                        self.say('You locked the door')
                        return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": "dumbwaiter workroom",
            "DOW": "dungeon",
        }
