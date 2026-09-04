""" handlers for the game """


from collections import deque

from utils.string_builder import StringBuilder
from utils.command_router import CommandRouter

# from data import ROOMS
from data import OBJECTS
from texts import TEXTS

from rooms.exchange import Exchange
from rooms.bed import Bed
from rooms.bedroom import Bedroom
from rooms.hall import Hall
from rooms.kitchen import Kitchen
from rooms.dumbwaiter_kitchen import DumbwaiterKitchen
from rooms.dumbwaiter_pantry import DumbwaiterPantry
from rooms.dumbwaiter_workroom import DumbwaiterWorkroom


class GameState:
    """ ... """

    _rooms: dict = None
    _output: deque = None
    _location: str = None
    _day: int = None
    # location: str = "bed"
    day: int = 1
    moves_to_sunset: int = 0

    _inventory: set = {'tent stake'}

    awake: bool = False
    game_over: bool = False

    @staticmethod
    def start():
        """ ... """

        output = Exchange.output
        GameState._output = output
        GameState._rooms = {
            "bed": Bed(),
            "bedroom": Bedroom(),
            "hall": Hall(),
            "kitchen": Kitchen(),
            "dumbwaiter_kitchen": DumbwaiterKitchen(),
            "dumbwaiter_pantry": DumbwaiterPantry(),
            "dumbwaiter_workroom": DumbwaiterWorkroom(),
        }

        GameState._location = "bed"
        GameState.day = 1
        GameState.moves_to_sunset = 0

        GameState._inventory = {'tent stake'}

        GameState.awake = False
        GameState.game_over = False

        output.append('[CLEAR]')
        output.append(TEXTS["INTRO"])

        router = CommandRouter()
        router.subscribe('enter', GameHandler.enter)
        router.handle('enter', 'bed')

    @staticmethod
    def inventory():
        """ ... """

        output = GameState._output
        bld, aln = StringBuilder.bld_aln()

        output.append("I'm carrying the following:")
        found = False
        for key, value in OBJECTS.items():
            if value['location'] == 'player':
                aln(value['name'])
                found = True

        if not found:
            aln("not a thing!")

        GameState._output.append(str(bld))

    @staticmethod
    def get_inventory(noun: str):
        """ ... """

        GameState._inventory.add(noun)

    @staticmethod
    def drop_inventory(noun: str):
        """ ... """

        if noun in GameState._inventory:
            GameState._inventory.remove(noun)
            return noun

        return None

    @staticmethod
    def rooms():
        """ ... """

        return GameState._rooms

    @staticmethod
    def current_room():
        """ ... """

        location = GameState._location
        result =  GameState._rooms.get(location, None)
        if result is None:
            output = GameState._output
            output.append(f"I can't find {location}")
            output.append("try 'reset'")
            return None
        return result

    @staticmethod
    def output() -> deque:
        """ ... """

        return GameState._output


game: GameState = GameState()


class GameHandler:
    """ ... """

    @staticmethod
    def do_command(verb: str, noun: str) -> bool:
        """ ... """

        # location = game.location
        room = GameState.current_room()
        if room.handle_command(verb=verb, noun=noun):
            return True

        return GameHandler.general(verb, noun, room.name)

    @staticmethod
    def general(verb: str, noun: str, location: str) -> bool:
        """ ... """

        output = GameState.output()
        router = CommandRouter()

        room = GameState.current_room()
        location = room.name

        match verb:
            case "GET":
                obj = noun[:3]

                for key, value in OBJECTS.items():
                    if value['location'] == location:
                        if key == obj:
                            value['location'] = 'player'
                            output.append(f'I got {value["name"]}')
                            return True

            case 'DROP':
                obj = noun[:3]
                for key, value in OBJECTS.items():
                    if key == obj:
                        if value['location'] == 'player':
                            value['location'] = location
                            output.append(f'I dropped {value["name"]}')
                            return True

                output.append("I don't have {noun}")
                return False

            case "AUTO":
                output.append(f"{verb} {noun} seen")
                router.handle('auto', noun)
                return True

        output.append(f"I can't {verb} {noun if noun else ''} in {location}")
        return False

    @staticmethod
    def enter(location: str) -> bool:
        """ ... """

        output = GameState.output()
        if location is None:
            output.append("I can't go in that direction.")
            return False

        GameState._location = location
        GameHandler.where()
        return True

    @staticmethod
    def where() -> bool:
        """ ... """

        room = GameState.current_room()
        if room is None:
            GameState.output().append("I am lost")
            return False

        bld, aln = StringBuilder.bld_aln()
        aln()
        aln(room.description)
        # fixed = room.get('fixed_objects', None)

        seen = False
        location = room.name
        for key, value in OBJECTS.items():
            if value['location'] == location:
                if not seen:
                    aln('I see:')
                    seen = True
                aln(value['name'])

        exits = room.exits
        if exits:
            aln("some exits are:")
            for direction in exits:
                aln(direction)
        else:
            aln("there are no exits")
            aln("try: restart")

        GameState.output().append(str(bld))
        return True

    # def dungeon_handler(verb: str, noun: str, location: str) -> str:
    #     """ ... """
    #
    #     _ = location
    #
    #     match verb:
    #         case "UP":
    #             return GameHandler.enter("workroom")
    #         case "HELP":
    #             if noun is None:
    #                 return "Problem with the pit?, try HELP PIT"
    #             if noun == 'PIT':
    #                 return "remember the bed"
    #         case "TIE":
    #             if noun == "SHEET":
    #                 return "To what"
    #
    #         case "TO":
    #             if noun == "RINGS":
    #                 item = game.drop_inventory("sheet")
    #                 if item is None:
    #                     return "I do not have a sheet"
    #                 rooms = game.rooms()
    #                 room = rooms.get(game.location, None)
    #                 obj: set = room['free_objects']
    #                 obj.add(item)
    #                 return "tied to rings"
    #
    #     return GameHandler.general(verb, noun, location)
