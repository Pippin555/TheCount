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
                if key is None:
                    output.append("Take or Get what?")
                    return True

                obj = game.object(key)
                if obj is None:
                    output.append(f"I don't know what {key} is")
                    return False

                if not obj.movable:
                    output.append(f"I can't carry {obj.name}")
                    return False

                if key == 'CIG':
                    if game.has(noun='PAC', location='player'):
                        obj.location = 'player'
                        output.append(f'I got a cigarette')

                elif obj.location == location:
                    obj.location = 'player'

                    if obj.plural:
                        what = obj.name
                    else:
                        what = f'a {obj.name}'
                    output.append(f'I got {what}')
                else:
                    name = NOUNS.get(key, key)
                    if not obj.plural:
                        name = 'a ' + name
                    output.append(f'I do not see {name}')
                return True

            case 'DRO':
                if key is None:
                    output.append("Drop what?")
                    return True

                if game.has(noun=key, location='player'):
                    if key == 'MIR' and location != 'bed':
                        output.append(f"The mirror shattered, that's 7 years bad luck!")
                        game.place('MIR', '', 'shattered')
                    else:
                        location = 'pillow'
                    game.place(noun=key, location=location)
                    obj = game.object(key)
                    output.append(f'I dropped the {obj.name} in the {location}')
                    return True

                else:
                    noun = NOUNS.get(key, noun)
                    output.append(f"I don't have {noun}")
                    return False

            case 'LIG':
                if key is None:
                    output.append("Light what?")
                    return True

                match key:
                    case 'TOR' | 'MAT' | 'CIG':
                        if game.has(noun=key, location='player'):
                            obj = game.object(key)
                            if obj is None:
                                output.append(f"I don't know what {key} is")
                                return False

                            game.place(key, 'player', 'lit')
                            output.append(f'I lit the {obj.name}')
                            return True

                        else:
                            noun = NOUNS.get(noun, noun)
                            output.append(f"I don't have a {noun}")
                            return False

            case "SMO":
                if key is None:
                    output.append("Smoke what?")
                    return True

                match key:
                    case 'CIG':
                        if game.has('CIG', 'player lit'):
                            # to be able to drop it
                            game.place("CIG", 'player')
                            return True

                        elif game.has('CIG', 'player'):
                            output.append("I have no lit cigarette")
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
                if key is None:
                    output.append("Eat what?")
                    return True

                match key:
                    case 'TAB':
                        obj = game.object('TAB')
                        if obj is None:
                            output.append('Object "tablets" does not exist')
                            return False

                        if not obj.location == 'player':
                            output.append('I do not have tablets')
                            return True

                        count = int(obj.state) - 1
                        if count < 0:
                            output.append('I am out of tablets')
                            return True

                        game.place('TAB', obj.location, str(count))

                        output.append(f'I ate a tablet')
                        output.append("I'm real PEPPY now!")
                        return True

            case "AUT":
                if noun.isnumeric():
                    router.handle('auto', noun)
                else:
                    output.append("Please specify a number 1 .. 10 for 'AUTO'")
                return True

            case "HEL":
                location = self._game.location
                output.append(f'Sorry, HELP is not implemented yet for {location}')
                return True

            case "SAV":
                if noun.isnumeric() if noun else False:
                    self.save(number=int(noun))
                else:
                    output.append("Please specify a number 1..10 for 'SAVE'")
                    output.append("not yet implemented")
                return True

            case "LOA":
                if noun.isnumeric() if noun else False:
                    self.load(number=int(noun))
                else:
                    output.append("Please specify a number 1..10 for 'LOAD'")
                    output.append("not yet implemented")
                return True

            case "WHE":
                output.append('-----')
                game.objects.sort(key=lambda obj: obj.name)
                for obj in game.objects:
                    pos = obj.location or 'hidden'
                    state = obj.state or ''
                    output.append(f'{obj.key:3} {obj.name}: {pos}, {state}')
                return True

            case _:
                output.append(f"Unimplemented verb: {verb}   ******")

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

        objs = room.inventory
        if objs:
            aln('I see:')
            for obj in objs:
                aln(obj)

        # already listed, check the object name, does it have a capital first character?
        # for obj in game.objects:
        #     if obj.location == room.name:
        #         state = f'{obj.state} ' if obj.state else ''
        #         aln(f'{state}{obj.name} ({obj.location})')

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
