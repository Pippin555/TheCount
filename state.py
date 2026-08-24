from parser import Parser
from handlers import game
from texts import TEXTS
from handlers import GameHandler


class StateMachine:
    """ ... """

    @staticmethod
    def do_command(command: str) -> str:
        """ ... """

        if command == "":
            return GameHandler.where()

        parsed = Parser.parse(command.upper())

        if parsed is None:
            return "I must be stupid, but I do not understand what you mean"

        verb, noun = parsed

        match verb[:3]:
            case "INV":
                return game.inventory()

            case "NOR" | "SOU" | "EAS" | "WES" | "RAI" | "LOW":
                return StateMachine.go(verb)

            case "QUI":
                game.location = 'exited'
                return "you have eduted the game, try: restart"

            case "RES":
                return game.start()

            case "UNK"| "PWR":
                return TEXTS[verb]

            case _:
                return GameHandler.do_command(verb, noun)

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
