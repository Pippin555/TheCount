""" game state machine """

from parser import Parser

from game_state import GameState

from game_handlers import GameHandler

from texts import TEXTS


class StateMachine:
    """ ... """

    def __init__(self,
                 game: GameState,
                 handler: GameHandler):
        """ ... """

        self._game = game
        self._output = game.output()
        self._handler = handler

    def do_command(self, command: str) -> bool:
        """ ... """

        output = self._output

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
                output.append(self._game.inventory())
                return True

            case "NOR" | "SOU" | "EAS" | "WES" | "RAI" | "LOW":
                self.go(verb)
                return True

            case "QUI":
                self._game.exited()
                output.append("you have exited the game, try: restart")
                return True

            case "RES":
                self.game = GameState()
                return True

            case "UNK" | "PWR":
                output.append(TEXTS[verb])
                return True

            case "LOO":
                GameHandler.where()
                return True

            case "CLE":
                output.append('[CLEAR]')
                return True

            case _:
                return self._handler.do_command(verb, noun)

    def go(self, noun: str) -> bool:
        """ ... """

        room = self._game.current_room
        exits = room.exits
        if exits is None:
            output = GameState.output()
            output.append("There are no exits")
            return False

        next = exits.get(noun, None)
        return GameHandler.enter(next)
