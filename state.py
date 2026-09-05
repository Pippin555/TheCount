""" game state """

from parser import Parser
from handlers import game, GameState
from texts import TEXTS
from handlers import GameHandler
from rooms.exchange import Exchange


class StateMachine:
    """ ... """

    @staticmethod
    def do_command(command: str) -> bool:
        """ ... """

        output = Exchange.output

        if command == "":
            command = "look"

        parsed = Parser.parse(command.upper())

        if parsed is None:
            output.append("I must be stupid, but I do not understand what you mean")

        if not isinstance(parsed, tuple):
            return True

        verb, noun = parsed

        match verb[:3]:
            case "INV":
                output.append(game.inventory())
                return True

            case "NOR" | "SOU" | "EAS" | "WES" | "RAI" | "LOW":
                StateMachine.go(verb)
                return True

            case "QUI":
                game.exited()
                output.append("you have exited the game, try: restart")
                return True

            case "RES":
                output.append(game.start())
                return True

            case "UNK"| "PWR":
                output.append(TEXTS[verb])
                return True

            case "LOO":
                GameHandler.where()
                return True

            case "CLE":
                output.append('[CLEAR]')
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
