from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class CommandType(Enum):
    Move = auto()
    Place = auto()
    Remove = auto()
    Lost = auto()


@dataclass
class Command():
    # Abstract class, don't instantiate a command
    pass


@dataclass
class Surrender(Command):
    pass


@dataclass
class Quit(Command):
    pass


@dataclass
class Remove(Command):
    at: int


@dataclass
class Move(Command):
    origin: int
    to: int


@dataclass
class Place(Command):
    to: int
