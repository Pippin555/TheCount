""" parser for The Count """

from sys import stderr

from data import VERBS
from data import NOUNS


def parse(command: str) -> tuple[str, str | None] | None:
    """ ... """

    words = command.upper().split()
    if len(words) == 0:
        print("""YOU COMMAND ME WITH 2 WORD ENGLISH
SENTENCES. I DO HAVE OVER A 120 WORD
VOCABULARY SO IF A WORD DOESN'T WORK
TRY ANOTHER!
SOME COMMANDS I KNOW: HELP, SAVE GAME, QUIT, SCORE, TAKE INVENTORY.""",
              file=stderr)
        return None

    if len(words) > 2:
        print("USE NO MORE THAN 2 WORDS!", file=stderr)
        return None

    verb = VERBS.get(words[0][:3], None)
    if verb is None:
        print("""ITS BEYOND MY POWER TO DO THAT""", file=stderr)
        return None

    if len(words) == 1:
        return verb, None

    noun = NOUNS.get(words[1][:3], None)
    if noun is None:
        print(f"""I DON'T KNOW WHAT {noun} IS""", file=stderr)
        return None

    noun = NOUNS.get(words[1])

    if verb is None or noun is None:
        return None

    return verb, noun