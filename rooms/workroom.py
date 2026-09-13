""" the 'workroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper


class Workroom(Room):
    """ 'Workroom' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'workroom'
        kwargs['description'] = 'I am in a workroom'
        kwargs['inventory'] = {'vent'}
        super().__init__(kwargs)

        self.help_verbs.update({'ENT', 'PIC', 'OPE', 'LOC', 'CLO'})
        self.door_obj = self._game.get_obj('DOO')

    @property
    def door_state(self) -> str:
        """ ... """

        return self.door_obj.state

    @door_state.setter
    def door_state(self, state: str):
        """ ... """

        self.door_obj.state = state

    @with_helper
    def handle_command(self,
                       verb:str,
                       noun: str | None,
                       callback: Callable):
        """ ... """

        match verb:
            case "ENT":
                match noun:
                    case None:
                        self.say("Enter what?")
                        return True
                    
                    case "DUM":
                        return callback('enter', 'dumbwaiter workroom')

                    case "VEN":
                        self.say("A spooky voice is heard")
                        self.say('You’re not the size of bat')
                        return True

                    case "DOO":
                        if self.door_state == 'locked':
                            self.say('The door is locked')
                            return True

                        elif self.door_state == 'closed':
                            self.say('The door is closed')
                            return True

                        return callback('enter', 'closet')

            case 'DOW':
                return callback('enter', 'dungeon')

            case "GO":
                match noun:
                    case None:
                        self.say("Go where?")
                        return True

                    case "DOW":
                        return callback('enter', 'dungeon')

            case "PIC":
                match noun:
                    case None:
                        self.say("Pick what?")
                        return True

                    case "LOC":
                        if self.door_state in ['open', 'closed']:
                            self.say('I already picked the lock of the door')
                            return True

                        if not self._game.has('CLI', 'player'):
                            self.say('I do not have a paperclip')
                            return True

                        if self.door_state == 'locked':
                            self.say('I picked the lock of the door')
                            self.door_state = 'closed'
                            return True

            case 'OPE':
                match noun:
                    case None:
                        self.say("Open what?")
                        return True

                    case "DOO":
                        if self.door_state == 'open':
                            self.say('The door was already open')
                            return True

                        elif self.door_state == 'locked':
                            self.say('The door is locked')
                            return True

                        if self.door_state == 'closed':
                            self.door_state = 'open'
                            self.say('I opened the door')
                            return True

            case 'CLO':
                match noun:
                    case None:
                        self.say("Close what?")
                        return True

                    case "DOO":
                        if self.door_state == 'open':
                            self.door_state = 'closed'
                            self.say('I closed the door')
                            return True

            case 'LOC':
                match noun:
                    case None:
                        self.say("Lock what?")
                        return True

                    case "DOO":
                        if self.door_state == 'closed':
                            self.door_state = 'locked'
                            self.say('You locked the door')
                            return True

                        self.say(f'The door is {self.door_state}')
                        return True
        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": "dumbwaiter workroom",
            "DOW": "dungeon",
        }
