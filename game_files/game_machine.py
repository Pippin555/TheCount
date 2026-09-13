""" game state machine """

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
                 handler: GameHandler,
                 delay: int | None = None):
        """ ... """

        self._game = game
        self._output = game.output()
        self._handler = handler
        self._delay = delay

    def do_command(self, command: str) -> bool:
        """ ... """

        output = self._output
        game = self._game

        day, move = game.next_move()

        match day:
            case 1:
                if move == game.moves_to_sunset + 3:
                    if not game.has('GAR'):
                        self._output.append("A bat settled on my shoulder and bit me in the neck")
                        self._output.append("I have turned into a Vampire")
                        self._handler.enter('lost')
                        return True
                    else:
                        self._output.append("... A bat flew by")
                        self._output.append("It smelled somthing strange and it laughed at me")

            case 3:
                if move == game.moves_to_sunset:
                    game.place('DRA', 'coffin')

        if game.sunset == 0:
            game.getting_late()

        if day == 2 and move == 24:
            game.package_arrives()

        if game.carry_count():
            ... # game.place('END', '')

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
                if name == 'bed':
                    if game.day == 3:
                        self._output.append("This adventure must be solved in 3 days. I am sorry, you lost")
                        self.location = 'home'
                        return True

                    output.append('I went to sleep')

                    day, _ = game.next_day()

                    # make the coffin and Dracula invisible again
                    game.place('COF', '')
                    game.place('DRA', '')

                    if day == 2:
                        if game.has('VIA', 'player'):
                            self._output.append("The vial was stolen!")
                        game.place('VIA', '')

                    if day == 3:
                        if game.has('PAC', 'player'):
                            self._output.append("The pack of cigarettes was stolen!")
                        game.place('PAC', '')

                else:
                    output.append(f"I should go to bed to sleep, I  am now here: {name}")

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
                            output.append(f'I have extinguised the {noun}')
                            return True
                        elif game.has(noun=key, location='player'):
                            output.append(f"The {noun} was already extinguised")
                            return True

            case 'MOV':
                result = CommandRouter().handle('moves')
                if isinstance(result, tuple):
                    self._game.day, self._game.moves = result

                return True

            case 'SIH':  # backdoor commands for debugging purposes

                warp_rooms = []
                VERBS['WAR'] = "WARP"
                for name, room in self._game.rooms.items():
                    key = name[:3].upper()
                    if key in NOUNS:
                        output.append(f"The {name} was already present as NOUN")
                    else:
                        NOUNS[key] = name
                        warp_rooms.append(name)

                output.append('Changed to SIHIR (magic) mode, available test rooms for WARP"')
                for name in warp_rooms:
                    output.append(name)
                return True

            case 'WAR':
                match noun:
                    case 'COF':
                        self.warp("coffin")
                        return True

                    case 'CRY':
                        self.warp("crypt")
                        return True

                    case 'COU':
                        self.warp("courtyard")

                    case _:
                        noun = NOUNS.get(key, noun)
                        return self.warp(noun)

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
        """ this function sets the environment to test the room and it enters that room """

        game = self._game
        match next:
            case 'crypt':
                # player has to GET/TAK CIG,
                # LIGht CIG
                # SMOke CIG
                game.place('PAC', 'player')

            case 'coffin':
                # on the first visit:
                # player has to LIGht CIGarette
                # SMOke CIGarette
                # CUT BOLt
                # WITh FILe
                game.place('CIG', 'player')
                game.place('FIL', 'player')

            case 'dungeon':
                game.place('SHE', 'player')

            case "workroom":
                game.place('CLI', 'workroom')

            case "courtyard":
                game.place('PKG', 'courtyard')

        self._handler.enter(location=next)
        return True
