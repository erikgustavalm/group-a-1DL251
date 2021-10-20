from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from color import Color
from scoreboard import Scoreboard


class CommandType(Enum):
    Move = auto()
    Place = auto()
    Remove = auto()
    Lost = auto()
    Draw = auto()


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

### COMMANDS FOR NETWORKED GAMES ###


@dataclass
class Draw(Command):
    pass


@dataclass
class Lost(Command):
    pass


@dataclass
class StartGame(Command):
    op_name: str
    your_color: Color


@dataclass
class GetName(Command):
    pass


@dataclass
class SetName(Command):
    name: str


@dataclass
class DisplayScoreboard(Command):
    scoreboard: Scoreboard


@dataclass
class GameIsFull(Command):
    pass


@dataclass
class OpponentDisconnected(Command):
    pass
