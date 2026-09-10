""" game state for the game """

from collections import deque

from jsons import dumps

from utils.string_builder import StringBuilder

from data import GO
from data import OBJECT_DATA

from texts import TEXTS

from rooms.exchange import Exchange

from rooms.bed import Bed
from rooms.bedroom import Bedroom
from rooms.bedroom_window import BedroomWindow
from rooms.flowerbed import Flowerbed
from rooms.hall import Hall
from rooms.kitchen import Kitchen
from rooms.dumbwaiter_kitchen import DumbwaiterKitchen
from rooms.dumbwaiter_pantry import DumbwaiterPantry
from rooms.dumbwaiter_workroom import DumbwaiterWorkroom
from rooms.pantry import Pantry
from rooms.draculas_bedroom import DraculasBedroom
from rooms.workroom import Workroom
from rooms.dungeon import Dungeon
from rooms.pit import Pit
from rooms.courtyard import Courtyard
from rooms.closet import Closet
from rooms.bathroom import Bathroom
from rooms.passage import Passage
from rooms.crypt import Crypt
from rooms.oven import Oven
from rooms.coffin import Coffin

from game_files.game_storage import GameStorage


class GameState:
    """ ... """

    def __init__(self):
        """ ... """

        self._output: deque = Exchange.output
        output = self._output

        kwargs = {'game': self, 'output': output}

        self._rooms = {
            "bed": Bed(kwargs),
            "bedroom": Bedroom(kwargs),
            "bedroom window": BedroomWindow(kwargs),
            "flowerbed": Flowerbed(kwargs),
            "hall": Hall(kwargs),
            "kitchen": Kitchen(kwargs),
            "oven": Oven(kwargs),
            "dumbwaiter kitchen": DumbwaiterKitchen(kwargs),
            "dumbwaiter pantry": DumbwaiterPantry(kwargs),
            "dumbwaiter workroom": DumbwaiterWorkroom(kwargs),
            "pantry": Pantry(kwargs),
            "Dracula's bedroom": DraculasBedroom(kwargs),
            "workroom": Workroom(kwargs),
            "dungeon": Dungeon(kwargs),
            "pit": Pit(kwargs),
            "courtyard": Courtyard(kwargs),
            "closet": Closet(kwargs),
            "bathroom": Bathroom(kwargs),
            "passage": Passage(kwargs),
            "crypt": Crypt(kwargs),
            "coffin": Coffin(kwargs),
        }

        self.objects = [GO(*data) for data in OBJECT_DATA]
        self._location = "bed"
        self.day = 1
        self.moves = 0
        self.moves_to_sunset = 30

        self._inventory = set()

        self.awake = False
        self.game_over = False

        output.append('[CLEAR]')
        output.append(TEXTS["INTRO"])
        GameStorage().register(label='state', save=self.save, load=self.load)

    @property
    def sunset(self) -> int:
        """ -1: day 0: sunset 1: night """

        def sign(x: int | float):
            return int(x > 0) - int(x < 0)

        return sign(self.moves - self.moves_to_sunset)

    def save(self):
        """ ... """

        local = {}
        for obj in self.objects:
            local[obj.key] = obj.location

        lst = [str(item) for item in self._inventory]
        local['inventory'] = lst
        local['location'] = self.location

        GameStorage().store_value(section='state',
                                  name='local',
                                  value = dumps(local))

    def load(self):
        """ ... """

        local = GameStorage().load_value(section='state',
                                         name='local',
                                         default=dumps({}))
        ...

    def inventory(self):
        """ ... """

        output: deque = self._output
        bld, aln = StringBuilder.bld_aln()

        output.append("I'm carrying the following:")
        found = False
        for obj in self.objects:
            if obj.location.startswith('player'):
                aln(obj.name)
                found = True

        if not found:
            aln("nothing!")

        output.append(str(bld))

    def get_inventory(self, noun: str):
        """ meaning: get object and add that to 'player' inventory """

        found = False
        for obj in self.objects:
            if obj.key == noun:
                found = True
                obj.location = 'player'

        if not found:
            self._output.append(f"I can't find {noun}")

        return found

    def drop_inventory(self, noun: str):
        """ ... """

        found = False
        for obj in self.objects:
            if obj.key == noun:
                found = True
                obj.location = self._location

        if not found:
            self._output.append(f"I don't have {noun}")

        return found

    def has(self,
            noun: str,
            location='player',
            state: str | None = None):
        """ ... """

        for obj in self.objects:
            if (obj.key == noun and
                    obj.location == location):
                if state is not None:
                    if obj.state == state:
                        return True
                return  True

        return False

    def object(self, noun: str):
        """ ... """

        for obj in self.objects:
            if obj.key == noun:
                return obj

        return None

    def place(self,
              noun: str,
              location='',
              state: str | None = None):
        """ ... """

        for obj in self.objects:
            if obj.key == noun:
                obj.location = location
                obj.state = state
                return True

        return False

    def carry_count(self) -> bool:
        """ ... """

        carried = []
        for obj in self.objects:
            if obj.location.startswith('player'):
                carried.append(obj.name)

        count = len(carried)
        if count > 6:
            self._output.append(f"Carrying too many items {count} > 6. ****")
            for name in carried:
                self._output.append(name)
            return True
        return False

    def next_day(self):
        """ ... """

        self.day += 1
        self.moves = 1

        # make the coffin invisible again
        self.place('COF', '')
        self.place('DRA', '')

    def next_move(self) -> tuple[int, int]:
        """ ... """

        self.moves += 1
        if self.day == 3:
            if self.moves == self.moves_to_sunset:
                self.place('DRA', 'coffin')

        return self.clock()

    def clock(self) -> tuple[int, int]:
        """ ... """

        return (self.day, self.moves)

    def getting_late(self):
        """ ... """

        self._output.append("It is getting dark and I am getting tired.")
        day, move = self.clock()
        self._output.append(f"It is day {day} and move {move}.")

    def package_arrives(self):
        """ ... """

        self._output.append("***")
        self._output.append("The bell at the front door was rung")

        if self.has(noun='PKG', location=''):
            self.place(noun='PKG', location='courtyard')

        self._output.append("***")
        self._output.append("")

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
