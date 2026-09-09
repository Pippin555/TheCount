""" game state machine """
from idlelib.colorizer import matched_named_groups

from parser import Parser

from game_files.game_state import GameState

from game_files.game_handlers import GameHandler

from texts import TEXTS

from data import NOUNS
from data import VERBS

from utils.string_builder import StringBuilder
from utils.command_router import CommandRouter


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
        output.append(f'* {day} {move}: {verb} {noun if noun else ""}')
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
                self._game = game = GameState()
                game.moves = 0
                self._handler = GameHandler(game=game)
                return True

            case "UNK" | "PWR":
                bld, aln = StringBuilder.bld_aln()
                aln(f'issue with: "{command}"')
                aln(TEXTS[verb])
                output.append(str(bld))
                return False

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

            case 'MOV':
                result = CommandRouter().handle('moves')
                if isinstance(result, tuple):
                    self._game.day, self._game.moves = result

                return True

            case 'SIH':
                VERBS['WAR'] = "WARP"
                NOUNS['COF'] = "COFFIN"
                NOUNS['CRY'] = "CRYPT"
                output.append('Changed to SIHIR mode,avaiable test rooms for WARP')
                output.append('crypt')
                output.append('coffin')
                return True

            case 'WAR':
                match noun:
                    case 'COF':
                        self.warp("coffin")
                        return True

                    case 'CRY':
                        self.warp("crypt")
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

    def warp(self, next: str):
        """ ... """

        game = self._game
        match next:
            case 'crypt':
                # game.location = 'crypt'
                game.place('PAC', 'player')
                # game.place("COF", 'crypt')

            case 'coffin':
                game.place('CIG', 'player')
                game.place('FIL', 'player')

        self._handler.enter(location=next)
        return True
