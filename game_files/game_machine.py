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
        game = self._game

        day, move = game.next_move()

        if game.sunset == 0:
            game.getting_late()

        if day == 2 and move == 24:
            game.package_arrives()

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
        key = noun[:3] if noun else None

        match verb:
            case "INV":
                output.append(self._game.inventory())
                return True

            case "GO":
                return self.go(key) if key else False

            case "NOR" | "SOU" | "EAS" | "WES" | "RAI" | "LOW":
                self.go(verb)
                return True

            case "QUI":
                game.exited()
                output.append("you have exited the game, try: restart")
                return True

            case "RES":
                game = game = GameState()
                game.moves = 0
                self._handler = GameHandler(game=game)
                return True

            case "UNK" | "PWR":
                bld, aln = StringBuilder.bld_aln()
                aln(f'issue with: "{command}"')
                aln(TEXTS[verb])
                output.append(str(bld))
                return False

            case "LOO":
                match noun:
                    case None:
                        self._handler.where()
                    case 'WAT':
                        output.append(f'day {game.day} move {game.moves}')

                return True

            case "CLE":
                output.append('[CLEAR]')
                return True

            case "SLE":
                room = game.current_room
                name = room.name
                if name == 'Bed':
                    output.append('You went to sleep')
                    game.next_day()
                else:
                    output.append(f"Go to bed to sleep, you are now here: {name}")

                return True

            case "WAI":
                output.append('some time goes by')
                return True

            case "EVE":
                game.moves = game.moves_to_sunset - 1
                return True

            case 'LIG':
                match key:
                    case 'TOR' | 'MAT':
                        if game.has(noun=key, location='player'):
                            game.place(key, 'player lit')
                            noun = NOUNS.get(key, noun)
                            output.append(f'You lit the {noun}')
                            return True
                        else:
                            noun = NOUNS.get(noun, noun)
                            output.append(f"I don't have a {noun}")
                            return False

            case 'EXT' | 'UNL':
                match key:
                    case 'TOR':
                        noun = NOUNS.get(key, key)
                        if game.has(noun=key, location='player lit'):
                            game.place(noun=key, location='player')
                            output.append(f'You have extinguised the {noun}')
                            return True
                        elif game.has(noun=key, location='player'):
                            output.append(f"The {noun} was already extinguised")
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
