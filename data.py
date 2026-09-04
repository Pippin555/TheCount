""" data file for The Count by Scott Adams """

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
    "QUI": "QUIT",
    "HEL": "HELP",
    "INV": "INVENTORY",
    "SCO": "SCORE",
    "RES": "RESTART",
    "DOW": "DOWN",
    "UP": "UP",
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
    "SHE": "SHE", # sheet
    "RIN": "RIN", # ring in the wall
}

# movable objects
OBJECTS = {
    "STA": {'name': 'tent stake', 'location': 'player'},
    "SHE": {'name': 'sheet', 'location': 'bedroom'},
}

ROOMS = {
    # "in bed": {
    #     "description": "I'm lying in a large brass bed",
    #     "fixed_objects": {"pillow"},
    #     "free_objects": {"sheet"},
    #     "exits": {"GET UP": None},
    # },
    #
    # "bedroom": {
    #     "description": "I'm in the bedroom",
    #     "exits": {"NOR": "hall"},
    #     "fixed_objects": {"bed"},
    #     "free_objects": {"sheet"}
    # },

    # "hall": {
    #     "description": "I'm in a hall",
    #     "exits": {
    #         "SOU": "bedroom",
    #         "NOR": "bathroom",
    #         "WES": "kitchen",
    #         "EAS": "courtyard",
    #     },
    # },

    "bathroom": {
        "description": "I'm in a bathroom",
        "exits": {
            "SOU": "hall"
        }
    },

    # "kitchen": {
    #     "description": "I'm in a kitchen",
    #     "exits": {
    #         "EAS": "hall",
    #         "WES": "dumbwaiter_kitchen"
    #     },
    #     "fixed_objects": {"dumbwaiter"},
    # },

    # "dumbwaiter_kitchen": {
    #     "description": "I'm in the middle dumb-waiter",
    #     "exits": {
    #         "RAISE": "dumbwaiter_pantry",
    #         "EAS": "kitchen",
    #         "LOWER": "dumbwaiter_workroom",
    #     },
    # },

    "dumbwaiter_pantry": {
        "description": "I'm in the raised dumb-waiter",
        "exits": {
            "EAS": "pantry",
            "LOWER": "dumbwaiter_kitchen",
        },
    },

    "pantry": {
        "description": "I'm in a pantry",
        "exits": {
            "WES": "dumbwaiter_pantry"
        },
        "fixed_objects": {"dumbwaiter"},
    },

    "dumbwaiter_workroom": {
        "description": "I'm in the lowered dumb-waiter",
        "exits": {
            "EAS": "workroom",
            "RAISE": "dumbwaiter_kitchen",
        },
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
            # "EAS": "dead",
        },
        "fixed_objects": {"iron rings in the wall"},
        "free_objects": set(),
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
