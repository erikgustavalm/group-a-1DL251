import random

from color import Color
from phase import Phase
from state import State

from board import Board
from dataclasses import dataclass
from commands import Move, RemoveAfterMill


@dataclass
class Player:
    name: str
    color: Color
    coins_left_to_place: int
    pieces: int


@dataclass
class GameState:
    player1: Player
    player2: Player
    board: Board
    current_turn: int
    current_player: Player

    def has_won(self) -> bool:
        pass

    def get_opponent(self) -> Player:
        if self.current_player == self.player1:
            return self.player2
        else:
            return self.player1

    def _end_turn(self):
        self.current_turn += 1
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    # board: (num_nodes, adjacent_nodes, mills)
    def __init__(self, player1: str, player2: str, board: (int, [[int]], [[int]])):
        self.player1 = Player(player1, Color.Empty, 11)
        self.player2 = Player(player2, Color.Empty, 11)
        self.board = Board(board[0], board[1], board[2])
        self.current_turn = 1

        if random.randint(1, 2) == 1:
            self.player1.color = Color.Black
            self.player2.color = Color.White
            self.current_player = self.player1
        else:
            self.player1.color = Color.White
            self.player2.color = Color.Black
            self.current_player = self.player2

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

    # ??? try_move was split in two, try_place_piece is for the first phase
    # when you only place down pieces, since the Move command takes an origin
    # We could instead use one function and ignore the origin for the first phase
    # OR it could be one function that takes a Command
    # and then choose what to do based on the type of the command
    def try_place_piece(self, to: int) -> State:
        # Can only place new pieces in phase one
        if self.current_phase() != Phase.One:
            return State.Invalid
        # and only at empty spots
        if self.board[to].color != Color.Empty:
            return State.Invalid

        if self.board.place(to, current_player):
            return State.CreatedMill

        self._end_turn()
        return State.Valid

    # NOTE renamed is_legal_move to try_move
    def try_move(self, move: Move) -> State:
        piece_origin = self.board[move.origin]
        piece_to = self.board[move.to]

        # State 1 is handled by try_place_piece
        if self.current_phase() == Phase.One:
            return State.Invalid

        # Can't move to a spot already occupied by our color
        if piece_to.color == current_player.color:
            return State.Invalid

        # can't move a piece that isn't ours
        if piece_origin.color != current_player.color:
            return State.Invalid

        if self.current_phase() == Phase.Two:
            # can move to an adjacent node
            if move.to in piece_origin.adjacents:
                if self.board.move_to(move.origin, move.to):
                    return State.CreatedMill
                self._end_turn()
                return State.Valid
            return State.Invalid
        elif self.current_phase() == Phase.Three:
            # can move anywhere
            if self.board.move_to(move.origin, move.to):
                return State.CreatedMill
            self._end_turn()
            return State.Valid
        assert False, "Unknown phase"

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
            self.board.remove(cmd_remove.at, self.get_opponent())
            self._end_turn()
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

        # We only found pieces that were part of mills, so it's a legal move
        self.board.remove(cmd_remove.at, self.get_opponent())
        self._end_turn()
        return True

    def get_piece_count(self, color: Color) -> int:
        if color == Color.Black:
            return self.board.num_black
        elif color == Color.White:
            return self.board.num_white
        assert False, "Unknown color (or empty)"

    def update_mills(self) -> bool:
        pass
