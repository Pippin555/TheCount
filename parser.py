""" parser for The Count """

from sys import stderr

from data import VERBS
from data import NOUNS

class Parser:
    """ ... """

    @staticmethod
    def translate(verb: str) -> str:
        """ ... """

        dct = { "N": "NOR",
                "E": "EAS",
                "S": "SOU",
                "W": "WES"}

        return dct.get(verb, verb)

    @staticmethod
    def parse(command: str) -> tuple[str, str | None] | None:
        """ ... """

        words = command.upper().split()
        if len(words) == 0:
            return "UNK", None

        if len(words) > 2:
            print("USE NO MORE THAN 2 WORDS!", file=stderr)
            return "TWO", None

        verb = VERBS.get(words[0][:3], None)
        if verb is None:
            return "PWR", None

        if len(words) == 1:
            return verb, None

        noun = words[1]
        if noun is None:
            return None, None

        obj = NOUNS.get(words[1][:3], None)
        if obj is None:
            return "UNK", None

        return verb, noun