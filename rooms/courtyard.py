""" the 'bedroom' as 'room' in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from typing import Callable

from rooms.room import Room
from rooms.room import with_helper


class Courtyard(Room):
    """ 'Hall' as 'room' in the game 'The Count' """

    def __init__(self, kwargs: dict):
        """ ... """

        kwargs['name'] = 'courtyard'
        kwargs['description'] = 'I am in a courtyard'
        kwargs['inventory'] = set()
        super().__init__(kwargs)
        self.help_verbs.update({'REA', 'OPE'})

    @with_helper
    def handle_command(self,
                       verb:str,
                       noun: str,
                       callback: Callable):
        """ ... """

        match verb:
            case'REA':
                match noun:
                    case 'POS':
                        self.say("Its for DRACULA, its and EATING & GHOULING bill from")  # noqa
                        self.say("a local mortuary!")
                        self.say("There's a note PAPER CLIPPED to the postcard")
                        self._game.place('NOT', 'player')
                        self._game.place('CLI', self.name)
                        return True

                    case 'NOT':
                        self.say("Postmaster says he'll be delivering a package tomorrow.")
                        return True

            case 'OPE':
                match noun:
                    case 'PAC':
                        # this is either PKG for the PACKAGE, when unopened
                        # or the PACK OF CIGARETTES when in possession
                        if self._game.has('PKG', 'courtyard') and \
                            self._game.has('PAC', 'package'):
                            # meaning: opened
                            self.say('I opened the package')
                            self.say('I see a pack of cigarettes')
                            return True

            case 'TAK' | 'GET':
                match noun:
                    case 'PAC':
                        self._game.place('PAC', 'player')
                        self.say('I got the pack of cigarettes')
                        return True

        return False

    @property
    def exits(self) -> dict:
        """ ... """

        return {
            "WES": "hall",
            # "EAS": "gate",
        }
