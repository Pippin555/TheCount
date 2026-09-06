""" handlers for the game """

from utils.string_builder import StringBuilder
from utils.command_router import CommandRouter

from game_state import GameState


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
        if room.handle_command(verb=verb, noun=noun):
            return True

        return self.general(verb, noun, room.name)

    def general(self,
                verb: str, noun: str,
                location: str) -> bool:
        """ ... """

        game = self._game
        output = self._output
        router = CommandRouter()

        key = noun[:3]

        match verb:
            case "GET" | "TAKE":
                for obj in game.objects:
                    if obj.key == key:
                        obj.location = 'player'
                        output.append(f'I got {obj.name}')
                        return True

            case 'DROP':
                for obj in game.objects:
                    if key == obj.key:
                        if obj.location == 'player':
                            obj.location = location
                            output.append(f'I dropped {obj.name} in {location}')
                            return True

                output.append(f"I don't have {noun}")
                return False

            case "AUTO":
                output.append(f"{verb} {noun} seen")
                router.handle('auto', noun)
                return True

        output.append(f"I can't {verb} {noun if noun else ''} in {location}")
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
