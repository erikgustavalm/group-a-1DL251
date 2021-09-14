from color import Color
from phase import Phase

from board import Board
from dataclasses import dataclass
from commands import Move, RemoveAfterMill


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

    # NOTE renamed is_legal_move to try_move
    def try_move(self, move: Move) -> bool:
        pass

    # NOTE renamed is_legal_remove to try_remove
    def try_remove(self, cmd_remove: RemoveAfterMill) -> bool:
        remove = self.board[cmd_remove.at]

        if remove.color == Color.Empty:
            return False
        if remove.color == current_player.color:
            return False

        # Is the piece we want to remove part of a mill?
        # If it isn't, it's always a legal move
        if not self.board.is_part_of_mill(cmd_remove.at):
            self.board.remove(cmd_remove.at)
            return True

        # if it is, we need to check if all other pieces of the same color
        # are part of mills, then it's a legal move

        # Loop through all the nodes that are of the same color
        # as the piece we're going to remove, figure out if
        # it's NOT part of a mill. If it isn't, the move is not legal.

        # NOTE Haven't thought this through very deeply, might be incorrect
        for idx, check in enumerate(self.board.nodes):
            if remove.color != check.color:
                continue

            if not self.board.is_part_of_mill(idx):
                return False

        # We only founds pieces that were part of mills, so it's a legal move
        self.board.remove(cmd_remove.at)
        return True

    def create_board(self) -> Board:
        pass

    def update_mills(self) -> bool:
        pass

    def current_phase(self, player: Player) -> Phase:
        if player.coins_left_to_place > 0:
            return Phase.One

        if player.color == Color.Black:
            num = self.board.num_black
        elif player.color == Color.White:
            num = self.board.num_white
        else:
            assert False, "Unknown player color, has to be Black or White"

        if num > 3:
            return Phase.Two
        return Phase.Three
