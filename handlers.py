from copy import deepcopy

from utils.string_builder import StringBuilder
from utils.command_router import CommandRouter

from data import ROOMS
from texts import TEXTS


class GameState:
    """ ... """

    _rooms: dict = deepcopy(ROOMS)
    location: str = "in bed"
    day: int = 1
    moves_to_sunset: int = 0

    _inventory: set = {'tent stake'}

    awake: bool = False
    game_over: bool = False

    @staticmethod
    def start():
        """ ... """

        GameState._rooms = deepcopy(ROOMS)
        GameState.location = "in bed"
        GameState.day = 1
        GameState.moves_to_sunset = 0

        GameState._inventory = {'tent stake'}

        GameState.awake = False
        GameState.game_over = False

        out = lambda msg: CommandRouter().handle('log', msg)

        out('[CLEAR]')
        out(TEXTS["INTRO"])
        out(GameHandler.enter('in bed'))

    @staticmethod
    def inventory():
        """ ... """

        bld, aln = StringBuilder.bld_aln()

        aln("I'm carrying the following:")
        if GameState._inventory:
            for item in GameState._inventory:
                aln(item)
        else:
            aln("not a thing!")

        return str(bld)

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


game: GameState = GameState()


class GameHandler:
    """ ... """

    @staticmethod
    def do_command(verb: str, noun: str) -> str:
        """ ... """

        location = game.location
        dct = {
            'in bed': GameHandler.in_bed_handler,
            'kitchen': GameHandler.kitchen_handler,
            'workroom': GameHandler.workroom_handler,
            'dungeon': GameHandler.dungeon_handler,
        }

        hnd = dct.get(game.location, GameHandler.general)
        return hnd(verb, noun, location)

    @staticmethod
    def general(verb: str, noun: str, location: str) -> str:
        """ ... """

        match verb:
            case "GET":
                rooms = game.rooms()
                room = rooms.get(game.location, None)
                free = room.get('free_objects', None)
                noun = noun.lower()
                if noun in free:
                    game.get_inventory(noun)
                    free.discard(noun)
                    return f'I got {noun}'

        return f"I can't {verb} {noun} in {location}"

    @staticmethod
    def enter(location: str) -> str:
        """ ... """

        if location is None:
            return "I can't go in that direction."

        game.location = location
        return GameHandler.where()

    @staticmethod
    def where() -> str:
        """ ... """
        rooms = game.rooms()
        location = game.location
        room = rooms.get(location, None)
        if room is None:
            return "I am lost"

        bld, aln = StringBuilder.bld_aln()
        aln()
        aln(room['description'])
        fixed = room.get('fixed_objects', None)
        free = room.get('free_objects', None)
        if free or fixed:
            aln("I see:")
            if fixed:
                for item in fixed:
                    aln(item)
            if free:
                for item in free:
                    aln(item)

        exits = room.get("exits", None)
        if exits:
            aln("some exits are:")
            for direction in exits:
                aln(direction)
        else:
            aln("there are no exits")
            aln("try: restart")

        return str(bld)

    @staticmethod
    def in_bed_handler(verb: str, noun: str, location: str) -> str:
        """ ... """

        _ = location

        if verb == "GET" and noun == "UP":
            return GameHandler.enter("bedroom")

        return GameHandler.general(verb, noun, location)

    @staticmethod
    def kitchen_handler(verb: str, noun: str, location: str) -> str:
        """ ... """

        _ = location

        if verb == "GO" and noun == "DUM":
            return GameHandler.enter("dumbwaiter_kitchen")

        return GameHandler.general(verb, noun, location)

    @staticmethod
    def workroom_handler(verb: str, noun: str, location: str) -> str:
        """ ... """

        _ = location

        if verb == "DOWN":
            return GameHandler.enter("dungeon")

        return GameHandler.general(verb, noun, location)

    @staticmethod
    def dungeon_handler(verb: str, noun: str, location: str) -> str:
        """ ... """

        _ = location

        match verb:
            case "UP":
                return GameHandler.enter("workroom")
            case "HELP":
                if noun is None:
                    return "Problem with the pit?, try HELP PIT"
                if noun == 'PIT':
                    return "remember the bed"
            case "TIE":
                if noun == "SHEET":
                    return "To what"

            case "TO":
                if noun == "RINGS":
                    item = game.drop_inventory("sheet")
                    if item is None:
                        return "I do not have a sheet"
                    rooms = game.rooms()
                    room = rooms.get(game.location, None)
                    obj: set = room['free_objects']
                    obj.add(item)
                    return "tied to rings"

        return GameHandler.general(verb, noun, location)
