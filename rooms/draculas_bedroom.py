""" the 'bed' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class DraculasBedroom(Room):
    """ 'Pantry' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = "Dracula's bedroom"
        kwargs['inventory'] = {"Dracula's Painting", "Window" }
        kwargs['description'] = "I am in Dracula's bedroom"
        super().__init__(kwargs)

    def handle_command(self,
                       verb: str,
                       noun: str,
                       callback: Callable) -> bool:
        """ ... """

        game = self._game
        match verb:
            case 'REM':
                match noun:
                    case 'POR':
                        if game.has('POR', 'hanging'):
                            self._inventory.clear()
                            self.say("I removed Dracula's portrait")
                            game.place('POR', 'player')
                            game.place('STA', self.name)
                            self._inventory.add('Passage')
                            self.say("I found a tent stake")
                            self.say("I found a passage")
                            return True

            case 'ENT':
                match noun:
                    case 'WIN':
                        return callback('enter', 'flowerbed')

                    case 'PAS':
                        if not game.has('POR', 'hanging'):
                            return callback('enter', 'passage')

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": 'flowerbed'
        }
