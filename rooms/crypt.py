""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room


class Crypt(Room):
    """ 'Hall' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):

        """ ... """

        kwargs['name'] = 'crypt'
        kwargs['description'] = 'I am in a crypt'
        kwargs['inventory'] = {'Sign'}
        super().__init__(kwargs)
        self.sunset = False

    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        game = self._game

        match verb:
            case 'LOO':
                match noun:
                    case 'SIG':
                        self.say("The sign says:")
                        self.say("POSITIVELY NO SMOKING ALLOWED HERE!")
                        self.say("Signed: Dracula")
                        self.wait_counter = 1
                        return True

            case 'WAI':
                self.say("Some time has passed")
                self.say("The sun has set")
                self.sunset = True

            case 'GET' | 'TAK':
                match noun:
                    case 'CIG':
                        if not self.sunset:
                            self.say("SMOKING IS BAD FOR YOUR HEALTH!")

                        elif game.has('PAC', 'player'):
                            game.place('CIG', 'player')
                            self.say('I took a cigarette')

            case "LIG":
                match noun:
                    case 'CIG':
                        if game.has('CIG', 'player'):
                            game.place("COF", self.name)
                            self.say("There is a Coughin here")

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            # "SOU": "bedroom",
            # "NOR": "bathroom",
            # "WES": "kitchen",
            "EAS": "passage",
        }
