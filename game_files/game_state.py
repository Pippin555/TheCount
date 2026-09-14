""" game state for the game """

from collections import deque

from os import makedirs

from os.path import abspath
from os.path import join
from os.path import isfile
from os.path import dirname

from jsons import dumps
from jsons import loads

from utils.string_builder import StringBuilder

from data import GO
from data import GameObject
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
from rooms.lost import Lost
from rooms.home import Home


class GameState:
    """ ... """

    def __init__(self):
        """ ... """

        self._output: deque = Exchange.output
        output = self._output

        self.objects = [GO(*data) for data in OBJECT_DATA]
        self.objects.extend([
            GameObject(key='BWW',
                       name="window_state",
                       location='bedroom',
                       plural=False,
                       movable=False,
                       state='closed'),

            GameObject(key='DOO',
                       name="workroom door",
                       location='workroom',
                       plural=False,
                       movable=False,
                       state='locked'),

            GameObject(key='DAY',
                       name="game_day",
                       location='',
                       plural=False,
                       movable=False,
                       state='1'),

            GameObject(key='MOV',
                       name="game_move",
                       location='',
                       plural=False,
                       movable=False,
                       state='0'),

            GameObject(key='LOC',
                       name="game_location",
                       location='',
                       plural=False,
                       movable=False,
                       state='bed'),
        ])

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
            "lost": Lost(kwargs),
            "home": Home(kwargs),
        }

        self._loc_obj = self.get_obj("LOC")
        self._day_obj = self.get_obj('DAY')
        self._mov_obj = self.get_obj('MOV')

        self.sunsets = [0, 40, 25, 35]
        self.moves_to_sunset = self.sunsets[self.day]

        output.append('[CLEAR]')
        output.append(TEXTS["INTRO"])

    def get_obj(self, key: str) -> GameObject | None:
        """ ... """

        for obj in self.objects:
            if obj.key == key:
                return obj

        return None

    @property
    def day(self) -> int:
        """ get the day of the game (starts at 1) """

        return int(self._day_obj.state)

    @day.setter
    def day(self, value: int):
        """ set the day of the game (starts at 1) """

        self._day_obj.state = str(value)

    @property
    def moves(self):
        """ get the current move of the game (starts at 1) """

        return int(self._mov_obj.state)

    @moves.setter
    def moves(self, value: int):
        """ set the current move of the game (starts at 0) """

        self._mov_obj.state = str(value)

    @property
    def location(self):
        """ get the current move of the game (starts at 1) """

        return self._loc_obj.state

    @location.setter
    def location(self, value: str):
        """ set the current location of the game (starts at 0) """

        self._loc_obj.state = value

    @property
    def sunset(self) -> int:
        """ -1: day 0: sunset 1: night """

        def sign(x: int | float):
            return int(x > 0) - int(x < 0)

        return sign(self.moves - self.moves_to_sunset)

    def inventory(self):
        """ ... """

        output: deque = self._output
        bld, aln = StringBuilder.bld_aln()

        output.append("I'm carrying the following:")
        found = False
        for obj in self.objects:
            if obj.location.startswith('player'):
                match obj.key:
                    case 'TAB' | 'CIG' | 'TOR' | 'PAC' | 'SHE':
                        state = f'{obj.state} ' if obj.state else ''
                        aln(f'{state}{obj.name} ({obj.location})')
                    case _:
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
                obj.location = self.location

        if not found:
            self._output.append(f"I don't have {noun}")

        return found

    def has(self,
            noun: str,
            location='player',
            state: str | None = None):
        """ ... """
        #
        # if ' ' in location:
        #     raise ValueError('has: location cannot contain space')

        for obj in self.objects:
            if (obj.key == noun and
                    obj.location == location):
                if state is not None:
                    return obj.state == state
                else:
                    return True

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

        # if ' ' in location:
        #     raise ValueError('place: location cannot contain space')

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

    def next_day(self) -> tuple[int, int]:
        """ ... """

        self.day += 1
        self.moves = 0
        self.moves_to_sunset = self.sunsets[self.day]

        return (self.day, self.moves)

    def next_move(self) -> tuple[int, int]:
        """ ... """

        self.moves += 1
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
    def current_room(self):
        """ ... """

        location = self.location
        result =  self._rooms.get(location, None)
        if result is None:
            output = self._output
            output.append(f"I can't find {location}")
            output.append("try 'RESTART' to play again")
            return None
        return result

    def output(self) -> deque:
        """ ... """

        return self._output

    def exited(self) -> None:
        """ ... """

        self.location = 'exited'

    def save(self, number: int):
        """ ... """

        value = dumps(self.objects)
        fname = join(abspath("."), "storage", f"save_{number:0>2}.json")
        makedirs(dirname(fname), exist_ok=True)

        with open(file=fname, mode='wt', encoding='utf-8') as stream:
            stream.write(value)

        self._output.append(f'Saved {fname}')

        return True

    def load(self, number: int):
        """ ... """

        fname = join(abspath("."), "storage", f"save_{number:0>2}.json")
        makedirs(dirname(fname), exist_ok=True)

        if isfile(fname):
            with open(file=fname, mode='rt', encoding='utf-8') as stream:
                work = loads(stream.read())

                for item in work:
                    target = self.get_obj(item['key'])
                    if target is not None:
                        target.location = item['location']
                        target.state = item['state']

            self.moves_to_sunset = self.sunsets[self.day]
            self._output.append(f'Loaded {fname}')
            return True

        else:
            self._output.append(f"I can't find {fname}")
            return False
