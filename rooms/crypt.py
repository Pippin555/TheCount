""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper


class Crypt(Room):
    """ 'Hall' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):

        """ ... """

        kwargs['name'] = 'crypt'
        kwargs['description'] = 'I am in a crypt'
        kwargs['inventory'] = {'Sign'}
        super().__init__(kwargs)
        self.help_verbs.update({'LIG', 'SMO', 'OPE', 'ENT'})

    @with_helper
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
                        return True

            case 'WAI':
                self.say("Some time has passed")
                return True

            case 'GET' | 'TAK':
                match noun:
                    case 'CIG':
                        # is it after sunset1 after 30 moves
                       if self._game.sunset == -1:
                            self.say("A spooky voice is heard:")
                            self.say("SMOKING IS BAD FOR YOUR HEALTH!")
                            self.say("(Wait till the sun has set)")
                            return True

                       elif game.has('PAC', 'player'):
                            game.place('CIG', 'player')
                            self.say('I took a cigarette')
                            return True

            case "LIG":
                match noun:
                    case 'CIG':
                        if game.has('CIG', 'player'):
                            if game.has('MAT', 'player'):
                                game.place('CIG', 'player lit')
                                self.say('I lit a cigarette')
                                return True
                            else:
                                self.say('I have no matches')
                                return True

                        self.say('I have no cigarette')
                        return True

            case "SMO":
                match noun:
                    case 'CIG':
                        if game.has('CIG', 'player lit'):
                            if game.has('COF', ''):
                                # reveal the coffin
                                game.place("COF", 'crypt')
                                self.say("There is a Coughin (sic!) here")  # noqa
                                # to be able to drop it
                                game.place("CIG", 'player')

                            return True

                        elif game.has('CIG', 'player') or game.has('CIG', ''):
                            self.say("I have no lit cigarette")
                            return True

            case "OPE":
                match noun:
                    case 'COF':
                        if game.has('COF', 'crypt open'):
                            return True

                        # when the coffin is revealed
                        if game.has('COF', 'crypt'):
                            game.place('COF', 'crypt open')
                            self.say('The coffin is open')
                            return True

            case "ENT":
                match noun:
                    case "COF":
                        if game.has('COF', ''):
                            self.say('There is no coffin')
                            return True

                        if game.has('COF', self.name):
                            self.say('The coffin is closed')
                            return True

                        if game.has('COF', self.name + ' open'):
                            return callback('enter', 'coffin')

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "SOU": "passage",
        }
