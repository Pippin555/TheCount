from parser import parse
from data import GameState
from data import ROOMS


class StateMachine:
    """ ... """

    @staticmethod
    def do_command(command: str) -> str:
        """ ... """

        parsed = parse(command.upper())

        if parsed is None:
            return "I MUST BE STUPID, BUT I JUST DON'T UNDERSTAND WHAT YOU MEAN"

        verb, noun = parsed

        match verb[:3]:
            case "GO":
                return StateMachine.go(noun)

            case "N" | "S" | "E" | "W" | "RAI" | "LOW":
                return StateMachine.go(verb)

            case "QUI":
                GameState.location = 'exited'
                return "YOU HAVE EXITED THE GAME"


    @staticmethod
    def go(noun: str) -> str:
        """ ... """

        current = GameState.location
        room = ROOMS[current]
        exits = room.exits
        next = exits.get(noun)
        if next is None:
            return "I CAN'T GO IN THAT DIRECTION."
        GameState.location = next
        return room['description']
