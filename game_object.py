""" a volatile object in the game 'The Count' """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2026-2026 all rights reserved"

from dataclasses import dataclass

@dataclass
class GameObject:
    """ a volatile object in the game """

    key: str = ''
    name: str = ''
    location: str = ''
