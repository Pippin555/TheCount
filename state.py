from collections import deque

from parser import Parser
from handlers import game
from texts import TEXTS
from handlers import GameHandler


class StateMachine:
    """ ... """

    @staticmethod
    def do_command(command: str, output: deque) -> bool:
        """ ... """

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
                output.append(StateMachine.go(verb))
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
                output.append(GameHandler.do_command(verb, noun))

    @staticmethod
    def go(noun: str) -> str:
        """ ... """

        current = game.location
        room = game.rooms()[current]
        exits = room.get('exits', None)
        if exits is None:
            return "There are no exits"

        next = exits.get(noun, None)
        return GameHandler.enter(next)
