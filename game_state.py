""" handlers for the game """

from collections import deque

from utils.string_builder import StringBuilder
from utils.command_router import CommandRouter

from data import GO
from data import OBJECT_DATA

from texts import TEXTS

from rooms.exchange import Exchange

# from game_handlers import GameHandler

from rooms.bed import Bed
# from rooms.bedroom import Bedroom
# from rooms.hall import Hall
# from rooms.kitchen import Kitchen
# from rooms.dumbwaiter_kitchen import DumbwaiterKitchen
# from rooms.dumbwaiter_pantry import DumbwaiterPantry
# from rooms.dumbwaiter_workroom import DumbwaiterWorkroom


class GameState:
    """ ... """

    def __init__(self):
        """ ... """

        self._output: deque = Exchange.output
        output = self._output

        # self._handler = GameHandler(game=self)

        self._rooms = {
            "bed": Bed(game=self, output=output),
            # "bedroom": Bedroom(game=self, output=output),
            # "hall": Hall(game=self, output=output),
            # "kitchen": Kitchen(game=self, output=output),
            # "dumbwaiter_kitchen": DumbwaiterKitchen(game=self, output=output),
            # "dumbwaiter_pantry": DumbwaiterPantry(game=self, output=output),
            # "dumbwaiter_workroom": DumbwaiterWorkroom(game=self, output=output),
        }
        self.objects = [GO(*data) for data in OBJECT_DATA]
        self._location = "bed"
        self.day = 1
        self.moves_to_sunset = 0

        self._inventory = set()

        self.awake = False
        self.game_over = False

        output.append('[CLEAR]')
        output.append(TEXTS["INTRO"])

        # note: this is a singleton
        router = CommandRouter()
        # needed fpr a restart:
        router.clear()

    def inventory(self):
        """ ... """

        output: deque = self._output
        bld, aln = StringBuilder.bld_aln()

        output.append("I'm carrying the following:")
        found = False
        for obj in self.objects:
            if obj.location == 'player':
                aln(obj.name)
                found = True

        if not found:
            aln("nothing!")

        output.append(str(bld))

    def get_inventory(self, noun: str):
        """ meaning: get object and add that to 'player' inventory """

        self._inventory.add(noun)

    def drop_inventory(self, noun: str):
        """ ... """

        if noun in self.inventory:
            self._inventory.remove(noun)
            return noun

        return None

    @property
    def rooms(self):
        """ ... """

        return self._rooms

    @property
    def location(self) -> str:
        """ ... """

        return self._location

    @location.setter
    def location(self, value: str) -> None:
        """ ... """

        self._location = value

    @property
    def current_room(self):
        """ ... """

        location = self._location
        result =  self._rooms.get(location, None)
        if result is None:
            output = self._output
            output.append(f"I can't find {location}")
            output.append("try 'restart'")
            return None
        return result

    def output(self) -> deque:
        """ ... """

        return self._output

    def exited(self) -> None:
        """ ... """

        self._location = 'exited'
