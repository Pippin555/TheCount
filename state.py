from collections import deque

from parser import Parser
from handlers import game, GameState
from texts import TEXTS
from handlers import GameHandler


class StateMachine:
    """ ... """

    @staticmethod
    def do_command(command: str) -> bool:
        """ ... """

        output = GameState.output()

        if command == "":
            output.append(GameHandler.where())
            return True

        parsed = Parser.parse(command.upper())

        if parsed is None:
            output.append("I must be stupid, but I do not understand what you mean")

        verb, noun = parsed

        match verb[:3]:
            case "INV":
                output.append(game.inventory())
                return True

            case "NOR" | "SOU" | "EAS" | "WES" | "RAI" | "LOW":
                StateMachine.go(verb)
                return True

            case "QUI":
                game.location = 'exited'
                output.append("you have exited the game, try: restart")
                return True

            case "RES":
                output.append(game.start())
                return True

            case "UNK"| "PWR":
                output.append(TEXTS[verb])
                return True

            case _:
                return GameHandler.do_command(verb, noun)

    @staticmethod
    def go(noun: str) -> bool:
        """ ... """

        room = game.current_room()
        exits = room.exits
        if exits is None:
            output = GameState.output()
            output.append("There are no exits")
            return False

        next = exits.get(noun, None)
        return GameHandler.enter(next)
