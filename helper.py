from enum import Enum

class Class(Enum):
    DEATH_KNIGHT = "C41E3A",
    DEMON_HUNTER = "A330C9",
    DRUID = "FF7C0A",
    EVOKER = "33937F",
    HUNTER = "AAD372",
    MAGE = "3FC7EB",
    MONK = "00FF98",
    PALADIN = "F48CBA",
    PRIEST = "FFFFFF",
    ROGUE = "FFF468",
    SHAMAN = "0070DD",
    WARLOCK = "8788EE",
    WARRIOR = "C69B6D",

class Type(Enum):
    TANK = 1,
    DPS = 2,
    HEALER = 3

class Faction(Enum):
    ALLIANCE = 1,
    HORDE = 2