from __future__ import annotations

from dataclasses import dataclass
from color import Color


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
class RemoveAfterMill(Command):
    at: int


@dataclass
class Move(Command):
    origin: int
    to: int


@dataclass
class Place(Command):
    to: int
