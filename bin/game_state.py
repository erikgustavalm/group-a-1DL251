from color import Color

from board import Board

@dataclass
class Player:
    name: str
    color: Color
    coins_left_to_place: int

@dataclass
class GameState:
    player1: Player
    player2: Player
    board: Board
    current_turn: int
    current_player: Player

    def is_legal_move(self, move: Move) -> bool:
        pass

    def is_legal_remove(self, remove: RemoveAfterMill) -> bool:
        pass

    def create_board(self) -> Board:
        pass

    def update_mills(self) -> bool:
        pass

    def current_phase(self, player: Player) -> int:
        pass