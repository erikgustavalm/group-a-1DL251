from dataclasses import dataclass
from color import Color


@dataclass
class Player:
    name: str
    color: Color = Color.Empty
    coins_left_to_place: int = 11
    pieces: int = 0
