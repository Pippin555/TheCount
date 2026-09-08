""" data file for The Count by Scott Adams """

from game_files.game_object import GameObject


VERBS = {
    "I": "INVENTORY",
    "N": "NORTH",
    "E": "EAST",
    "S": "SOUTH",
    "W": "WEST",
    "NOR": "NORTH",
    "EAS": "EAST",
    "SOU": "SOUTH",
    "WES": "WEST",
    "FLY": "FLY",
    "CLO": "CLOSE",
    "SHU": "SHUT",
    "OPE": "OPEN",
    "LIF": "LIFT",
    "RAI": "RAISE",
    "SLE": "SLEEP",
    "REA": "READ",
    "TO": "TO",
    "LOC": "LOCK",
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
    "PIC": "PICK",
    "REM": "REMOVE",
    "CLE": "CLEAR",
    "WHE": "WHEREIS",
    "EVE": "EVENING",
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
    "SHE": "sheet", # sheet
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
    "BED": "bed",
    "PAI": "painting of Dracula",
    "NOR": "North",
    "EAS": "Eath",
    "SOU": "South",
    "WES": "West",
    "ROO": "Room",
    "DOW": "Down",
    "VEN": "Vent",
    "PAS": "Passage",
    "SIG": "Sign",
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
    # key, name, location, plural
    ('SHE', 'sheet', 'bed', False),
    ('END', 'end of sheet', '', False),
    ('GAR', 'clove of garlic', 'pantry', False),
    ('MAT', 'matches', 'pantry', True),
    ('TOR', 'torch', '', False),
    ('PAC', 'pack of cigarettes', 'package', False),
    ('PKG', 'package', '', False),
    ('STA', 'tent stake', '', False),
    ('POS', 'postcard', 'courtyard', False),
    ('NOT', 'note', '', False),
    ('CLI', 'clip', '', False),
    ('VIA', 'vial', 'closet', False),
    ('TAB', 'tablets', 'closet', False),
    ('POR', "Dracula's portrait", "hanging", False),
    ('CIG', 'cigarette', '', False),
    ('FIL', 'broad file', 'oven', False),
    ('COF', "Coffin", "", False)
]


# obsolete
ROOMS = {

    "bathroom": {
        "description": "I'm in a bathroom",
        "exits": {
            "SOU": "hall"
        }
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
