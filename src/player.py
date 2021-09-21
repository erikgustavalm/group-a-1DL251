from dataclasses import dataclass
from color import Color

@dataclass
class Player:
    name: str
    color: Color
    coins_left_to_place: int
    pieces: int = 0