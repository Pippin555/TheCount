""" handlers for the game """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from data import NOUNS
from data import VERBS

from utils.string_builder import StringBuilder
from utils.command_router import CommandRouter

from game_files.game_state import GameState
from game_files.game_storage import GameStorage


class GameHandler:
    """ ... """

    def __init__(self, game: GameState):
        """ ... """

        self._game = game
        self._output = game.output()

        router = CommandRouter()
        router.subscribe('enter', self.enter)
        router.handle('enter', 'bed')

    def do_command(self, verb: str, noun: str) -> bool:
        """ ... """

        room = self._game.current_room
        verb = verb[:3]
        noun = noun[:3] if noun else None
        if room.handle_command(verb=verb,
                               noun=noun,
                               callback=self.handle_callback):
            return True

        return self.general(verb, noun, room.name)

    def general(self,
                verb: str, noun: str,
                location: str) -> bool:
        """ ... """

        game = self._game
        output = self._output
        router = CommandRouter()

        key = noun[:3] if noun else None

        match verb:
            case "GET" | "TAK":
                for obj in game.objects:
                    if obj.key == key:
                        if not obj.movable:
                            output.append(f"I can't carry {noun if noun else 'that'}")
                            return False

                        obj.location = 'player'

                        if obj.plural:
                            what = obj.name
                        else:
                            what = f'a {obj.name}'
                        output.append(f'I got {what}')
                        return True

            case 'DRO':
                if self._game.has(noun=key, location='player'):
                    self._game.place(noun=key, location=location)
                    name = NOUNS.get(key, noun)
                    output.append(f'I dropped the {name} in the {location}')
                    return True

                else:
                    noun = NOUNS.get(key, noun)
                    output.append(f"I don't have {noun}")
                    return False

            case 'LIG':
                match key:
                    case 'TOR' | 'MAT' | 'CIG':
                        if game.has(noun=key, location='player'):
                            game.place(key, 'player lit')
                            noun = NOUNS.get(key, noun)
                            output.append(f'You lit the {noun}')
                            return True
                        else:
                            noun = NOUNS.get(noun, noun)
                            output.append(f"I don't have a {noun}")
                            return False

            case "SMO":
                match noun:
                    case 'CIG':
                        if game.has('CIG', 'player lit'):
                            # to be able to drop it
                            game.place("CIG", 'player')
                            return True

                        elif game.has('CIG', 'player'):
                            self.say("I have no lit cigarette")
                            return False

            case "LOO":
                match key:
                    case None:
                        self.where()

                    case 'WAT':
                        output.append(f'day {game.day} move {game.moves}')
                        output.append(f'moves to sunset {game.moves_to_sunset}')
                        output.append(f'sunset: {game.sunset}')

                return True

            case 'EAT':
                noun = NOUNS.get(key, noun)
                match key:
                    case 'TAB':
                        output.append(f'You ate the {noun}')
                        return True

            case "AUT":
                if noun.isnumeric():
                    router.handle('auto', noun)
                else:
                    output.append("Please specify a number for 'AUTO'")
                return True

            case "HEL":
                output.append('Sorry, HELP is not implemented yet')
                return True

            case "SAV":
                if noun.isnumeric() if noun else False:
                    self.save(number=int(noun))
                else:
                    output.append("Please specify a number 1..10 for 'SAVE'")
                return True

            case "LOA":
                if noun.isnumeric() if noun else False:
                    self.load(number=int(noun))
                else:
                    output.append("Please specify a number 1..10 for 'LOAD'")
                return True

            case "WHE":
                output.append('-----')
                for obj in game.objects:
                    pos = obj.location or 'hidden'
                    output.append(f'{obj.key:3} {obj.name}: {pos}')

                return True

        verb = VERBS.get(verb, verb)
        noun = NOUNS.get(noun, noun)
        output.append(f"I can't {verb} {noun if noun else ''} in {location}")
        return False

    def save(self, number: int):
        """ ... """

        GameStorage().save(number=number)

    def load(self, number: int):
        """ ... """

        GameStorage().load(number=number)

    def handle_callback(self, verb: str, noun: str) -> bool:
        """ ... """

        match verb:
            case 'enter':
                return self.enter(location=noun)

        return False

    def enter(self, location: str | None) -> bool:
        """ ... """

        game = self._game
        output = self._output
        if location is None:
            output.append("I can't go in that direction.")
            return False

        game._location = location
        self.where()
        return True

    def where(self) -> bool:
        """ ... """

        output = self._output
        game = self._game
        room = game.current_room
        if room is None:
            output.append("I am lost")
            return False

        bld, aln = StringBuilder.bld_aln()
        aln('')
        aln(room.description)
        # fixed = room.get('fixed_objects', None)

        objs = room.inventory
        if objs:
            aln('I see:')
            for obj in objs:
                aln(obj)

        exits = room.exits
        if exits:
            aln("some exits are:")
            for direction in exits:
                aln(direction)
        else:
            aln("there are no exits")
            aln("try: restart")

        output.append(str(bld))
        return True
