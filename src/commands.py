from __future__ import annotations

from dataclasses import dataclass
from color import Color


@dataclass
class Command():
    # Abstract class, don't instantiate a command
    color: Color

    def validate(self, input: str) -> bool:
        pass

    def make(self, input: str) -> Command:
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
