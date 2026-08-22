""" data file for The Count by Scott Adams """
from dataclasses import dataclass

from dataclasses import dataclass
from dataclasses import field


VERBS = {
    "FLY": "FLY",
    "CLO": "CLOSE",
    "SHU": "SHUT",
    "OPE": "OPEN",
    "LIF": "LIFT",
    "RAI": "RAISE",
    "SLE": "SLEEP",
    "REA": "READ",
    "TO": "TO",
    "UNL": "UNLOCK",
    "EXT": "EXTINGUISH",
    "LIG": "LIGHT",
    "BUR": "BURN",
    "IGN": "IGNORE",
    "JUM": "JUMP",
    "WAI": "WAIT",
    "EMP": "EMPTY",
    "SPI": "SPIN",
    "CUT": "CUT",
    "GO": "GO",
    "GET": "GET",
    "TAK": "TAKE",
    "LOO": "LOOK",
    "EXA": "EXAMINE",
    "USE": "USE",
    "PUT": "PUT",
    "DRO": "DROP",
    "TIE": "TIE",
    "UNT": "UNTIE",
    "BRE": "BREAK",
    "PUL": "PULL",
    "LOW": "LOWER",
    "CLI": "CLIMB",
    "EAT": "EAT",
    "DRI": "DRINK",
    "SMO": "SMOKE",
    "KIL": "KILL",
    "ATT": "ATTACK",
    "SAV": "SAVE",
    "QUI": "QUIT",
    "HEL": "HELP",
    "INV": "INVENTORY",
    "SCO": "SCORE",
}

NOUNS = {
    "STA": "tent stake",
    "GAR": "dusty clove of garlic",
    "MAL": "rubber mallet",
    "MIR": "mirror",
    "WAT": "pocket watch",
    "TOR": "torch",
    "MAT": "sulfur matches",
    "FIL": "large tempered nail file",
    "PAC": "package",
    "CIG": "cigarette",
    "BOT": "bottle of Type V blood",
    # ...
}

ROOMS = {
    "bedroom": {
        "description": "I'm lying in a large brass bed",
        "exits": {"N": "hall"},
    },

    "hall": {
        "description": "I'm in a hall",
        "exits": {
            "S": "bedroom",
            "N": "bathroom",
            "W": "kitchen",
            "E": "courtyard",
        },
    },

    "bathroom": {
        "description": "I'm in a bathroom",
        "exits": {
            "S": "hall"
        }
    },

    "kitchen": {
        "description": "I'm in a kitchen",
        "exits": {
            "E": "hall",
            "W": "dumb_waiter_kitchen"
        }
    },

    "dumbwaiter_kitchen": {
        "description": "I'm in the dumb-waiter",
        "exits": {
            "RAI": "dumbwaiter_pantry",
            "E": "kitchen",
            "LOW": "dumbwaiter_workroom",
        },
    },

    "dumbwaiter_pantry": {
        "description": "I'm in the dumb-waiter",
        "exits": {
            "E": "pantry",
            "LOW": "dumbwaiter_kitchen",
        },
    },

    "pantry": {
        "description": "I'm in a pantry",
        "exits": {
            "W": "dumbwaiter_pantry"
        }
    },

    "dumbwaiter_workroom": {
        "description": "I'm in the dumb-waiter",
        "exits": {
            "E": "workroom",
            "RAI": "dumbwaiter_kitchen",
        },
    },

    "workroom": {
        "description": "I'm in a workroom",
        "exits": {
            "W": "dumbwaiter_workroom",
        },
    },

    "courtyard": {
        "description": "I'm outside the castle",
        "exits": {
            "W": "hall"
        }
    },

    "closet": {
        "description": "I'm in a closet",
    },

    "dungeon": {
        "description": "I'm in a dungeon",
    },

    "pit": {
        "description": "I'm in a pit",
    },

    "crypt": {
        "description": "I'm in a crypt",
    },

    "dark_passage": {
        "description": "I'm in a dark passage",
    },
}


@dataclass
class GameState:
    """ ... """

    location: str = "bedroom"
    day: int = 1
    moves_to_sunset: int = 0

    inventory: set[str] = field(default_factory=set)

    awake: bool = False
    game_over: bool = False