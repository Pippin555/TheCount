""" data file for The Count by Scott Adams """

from game_object import GameObject


VERBS = {
    "I": "INVENTORY",
    "N": "NOR",
    "E": "EAS",
    "S": "SOU",
    "W": "WES",
    "NOR": "NOR",
    "EAS": "EAS",
    "SOU": "SOU",
    "WES": "WES",
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
    "LOA": "LOAD",
    "QUI": "QUIT",
    "HEL": "HELP",
    "INV": "INVENTORY",
    "SCO": "SCORE",
    "RES": "RESTART",
    "DOW": "DOWN",
    "UP": "UP",
    "AUT": "AUTO",
    "ENT": "ENTER",
    "WIT": "WITH",
    # "SMO": "OPEN",
    "PIC": "PICK",
    "REM": "REMOVE",
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
    "UP": "get up",
    "DUM": "dumbwaiter",
    "PIT": "pit of death",
    "SHE": "sheets", # sheet
    "RIN": "ring", # ring in the wall
    "POS": "postcard",
    "CLI": "paperclip",
    "NOT": "note",
    "VIA": "vial",
    "TAB": "tablets",
    "DOO": "door",
    "LOC": "lock",
    "OVE": "oven",
    "POR": "portrait",
    "WIN": "window",
    "COF": "coffin",
    "BOL": "bolt",
    "DRA": "Dracula",
    "END": "end",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "10": "10",
}

GO = GameObject

# movable objects
OBJECT_DATA = [
    # key, name, location
    ('SHE', 'sheets', 'bed'),
    ('GAR', 'clove of garlic', 'pantry'),
    ('MAT', 'matches', 'pantry'),
    ('TOR', 'torch', 'cellar'),
    ('PAC', 'pack of cigarettes', 'package'),
    ('PKG', 'package', 'gate'),
]


# obsolete
ROOMS = {

    "bathroom": {
        "description": "I'm in a bathroom",
        "exits": {
            "SOU": "hall"
        }
    },

    "pantry": {
        "description": "I'm in a pantry",
        "exits": {
            "WES": "dumbwaiter_pantry"
        },
        "fixed_objects": {"dumbwaiter"},
    },

    "workroom": {
        "description": "I'm in a workroom",
        "exits": {
            "WES": "dumbwaiter_workroom",
            "DOW": "dungeon",
        },
        "fixed_objects": {"dumbwaiter"},
    },

    "courtyard": {
        "description": "I'm outside the castle",
        "exits": {
            "WES": "hall",
            "EAS": "castle gates",
        }
    },

    "castle gates": {
        "description": "I'm outside the castle gates",
        "exits": {
            "WES": "courtyard",
            "EAS": "dead",
        },
        "fixed_objects": {"a large group of angry peasants"},
    },

    "dead": {
        "description": "I was killed by the angry peasants",
        "fixed_objects": {"a gravestone with the text 'Adventurer'"}
    },

    "closet": {
        "description": "I'm in a closet",
    },

    "dungeon": {
        "description": "I'm in a dungeon",
        "exits": {
            "UP": "workroom",
        },
        "fixed_objects": {"iron rings in the wall"},
        "free_objects": set(),
    },

    "cellar": {
        "description": "I'm in a dark cellar",
    },

    "crypt": {
        "description": "I'm in a crypt",
    },

    "dark_passage": {
        "description": "I'm in a dark passage",
    },
}
