""" game state machine """

from parser import Parser

from game_files.game_state import GameState

from game_files.game_handlers import GameHandler

from texts import TEXTS

from data import NOUNS

from utils.string_builder import StringBuilder


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
            return True

        if not isinstance(parsed, tuple):
            return True

        verb, noun = parsed
        output.append(f'* {verb} {noun if noun else ""}')
        verb = verb[:3]

        match verb:
            case "INV":
                output.append(self._game.inventory())
                return True

            case "GO":
                if noun:
                    self.go(noun[:3])
                    return True
                return False

            case "NOR" | "SOU" | "EAS" | "WES" | "RAI" | "LOW":
                self.go(verb)
                return True

            case "QUI":
                self._game.exited()
                output.append("you have exited the game, try: restart")
                return True

            case "RES":
                self._game = game = GameState()
                self._handler = GameHandler(game=game)
                return True

            case "UNK" | "PWR":
                bld, aln = StringBuilder.bld_aln()
                aln(f'issue with: "{command}"')
                aln(TEXTS[verb])
                output.append(str(bld))
                return False

            case "LOO":
                self._handler.where()
                return True

            case "CLE":
                output.append('[CLEAR]')
                return True

            case "SLE":
                room = self._game.current_room
                name = room.name
                if name == 'Bed':
                    output.append('You went to sleep')
                else:
                    output.append(f"Go to bed to sleep, you are now here: {name}")

                return True

            case "WAI":
                output.append('some time goes by')
                return True

            case 'LIG':
                match noun[:3]:
                    case 'TOR' | 'MAT':
                        self._game.place(noun, 'player lit')
                        noun = NOUNS.get(noun, noun)
                        output.append(f'You lit the {noun}')
                        return True

            case 'EXT':
                match noun:
                    case 'TOR':
                        output.append('You extinguished the TORCH')
                        self._game.place('TOR', 'player')
                        return True

            case 'EAT':
                match noun[:3]:
                    case 'TAB':
                        noun = NOUNS.get(noun, noun)
                        output.append(f'You ate the {noun}')
                        return True

            case _:
                return self._handler.do_command(verb, noun)

    def go(self, noun: str) -> bool:
        """ ... """

        game = self._game
        handler = self._handler
        output = game.output()
        room = game.current_room

        exits = room.exits
        if exits is None:
            output.append("There are no exits")
            return False

        next = exits.get(noun, None)
        return handler.enter(location=next)
