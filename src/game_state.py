import random
from typing import List, Tuple

from color import Color
from phase import Phase
from state import State
from bot import Bot,Difficulty
from board import Board
from player import Player
from dataclasses import dataclass
from commands import Command, Move, Place, Remove, CommandType
from graphics import GraphicsHandler


@dataclass
class GameState:
    player1: Player
    player2: Player
    board: Board
    current_turn: int
    current_player: Player
    max_turns: int = 250
    _did_create_mill: bool = False

    def get_opponent(self) -> Player:
        if self.current_player == self.player1:
            return self.player2
        else:
            return self.player1

    def _end_turn(self):
        self._did_create_mill = False
        self.current_turn += 1
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def __set_color(self, black: Player, white: Player):
        black.color = Color.Black
        white.color = Color.White
        self.current_player = black

    def __init__(self,
                 player1: str,
                 player2: str,
                 # board: (num_nodes, adjacent_nodes, mills)
                 board: Tuple[int, List[List[int]], List[List[int]]],
                 player1_color: Color = None):

        self.board = Board(board[0], board[1], board[2])
        self.current_turn = 1

        # Empty string means that the player will be bot controlled
        if player1 == "easy":
            self.player1 = Bot(self.board, Color.Empty, 11)
        elif player1 == "medium":
            self.player1 = Bot(self.board, Color.Empty, 11, Difficulty.Medium)
        elif player1 == "hard":
            self.player1 = Bot(self.board, Color.Empty, 11, Difficulty.Hard)
        else:
            self.player1 = Player(player1, Color.Empty, 11)

        if player2 == "easy":
            self.player2 = Bot(self.board, Color.Empty, 11)
        elif player2 == "medium":
            self.player2 = Bot(self.board, Color.Empty, 11, Difficulty.Medium)
        elif player2 == "hard":
            self.player2 = Bot(self.board, Color.Empty, 11, Difficulty.Hard)
        else:
            self.player2 = Player(player2, Color.Empty, 11)

        if player1_color is None:
            self.__set_color(*random.sample([self.player1, self.player2], k=2))
        elif player1_color == Color.Black:
            self.__set_color(black = self.player1, white = self.player2)
        elif player1_color == Color.White:
            self.__set_color(black = self.player2, white = self.player1)
        else:
            assert False, f"Invalid value: '{player1_color}'"

    def can_make_adjacent_move(self, player: Player):
        node_indexes = self.board.get_player_nodes(player)
        for idx in node_indexes:
            for adjacent in self.board.nodes[idx].adjacents:
                if self.board.nodes[adjacent].color == Color.Empty:
                    return True
        return False

    def has_lost(self) -> bool:
        player = self.current_player
        if (player.coins_left_to_place > 0
                or self.get_opponent().coins_left_to_place > 0):
            return False

        if player.pieces < 3:
            return True
        phase = self.current_phase(player)
        if phase == Phase.Two and not self.can_make_adjacent_move(player):
            return True
        return False

    def is_draw(self) -> bool:
        # If we've exceeded the maximum number of turns, it's a draw.
        if self.current_turn > self.max_turns:
            return True

        # If the board is full, neither player can move, so it's a draw.
        if (self.player1.pieces + self.player2.pieces == self.board.num_nodes()):
            return True

        return False

    def next(self) -> CommandType:
        if self.is_draw():
            return CommandType.Draw
        if self.has_lost():
            return CommandType.Lost
        if self._did_create_mill:
            return CommandType.Remove

        phase = self.current_phase(self.current_player)
        if phase == Phase.One:
            return CommandType.Place
        return CommandType.Move

    def current_phase(self, player: Player) -> Phase:
        if player.coins_left_to_place > 0:
            return Phase.One
        if player.pieces > 3:
            return Phase.Two
        return Phase.Three

    def try_command(self, cmd: Command, gh: GraphicsHandler) -> State:
        res = None
        prev_current = self.current_player.name
        if isinstance(cmd, Place):
            res = self._try_place_piece(cmd, gh)
            if res == State.CreatedMill:
                gh.add_message(f"   [ Player {prev_current} - got a mill! ]")
            elif res == State.Valid:
                gh.add_message(f"   [ Player {prev_current} - piece placed on node {cmd.to+1} ]")
        elif isinstance(cmd, Move):
            res = self._try_move(cmd, gh)
            if res == State.CreatedMill:
                gh.add_message(f"   [ Player {prev_current} -  got a mill! ] ")
            elif res == State.Valid:
                gh.add_message(
                    f"   [ Player {prev_current} -  piece moved from node {cmd.origin+1} to node {cmd.to+1} ]")
        elif isinstance(cmd, Remove):
            res = self._try_remove(cmd, gh)
            if res == State.Valid:
                gh.add_message(
                    f"   [ Player {prev_current} -  removed opponent's piece at node {cmd.at+1} ]")
        else:
            assert False, f"   [ Invalid command: {cmd} ]"
        return res

    def _try_place_piece(self, to: Place, gh: GraphicsHandler) -> State:
        # Can only place new pieces in phase one
        if self.current_phase(self.current_player) != Phase.One:
            assert False, "   [ Bug: Can only place new pieces in phase one ]"
        # and only at empty spots
        if self.board.nodes[to.to].color != Color.Empty:
            gh.add_message("   [ Invalid: Can't place piece on occupied node. ]")
            return State.Invalid

        if self.board.place(to.to, self.current_player):
            self._did_create_mill = True
            return State.CreatedMill

        self._end_turn()
        return State.Valid

    def _try_move(self, move: Move, gh: GraphicsHandler) -> State:
        piece_origin = self.board.nodes[move.origin]
        piece_to = self.board.nodes[move.to]

        # State 1 is handled by try_place_piece
        if self.current_phase(self.current_player) == Phase.One:
            assert False, "   [ Bug: Can't move piece if not in phase 1. ]"

        if (self.current_phase(self.current_player) == Phase.Two
            and move.to not in piece_origin.adjacents):
            gh.add_message(
                "   [ Invalid: Can't move piece to a node that's not adjacent.")
            return State.Invalid

        if piece_to.color != Color.Empty:
            gh.add_message("   [ Invalid: Can't move piece to node that's already occupied.")
            return State.Invalid

        if piece_origin.color != self.current_player.color:
            gh.add_message(
                "   [ Invalid: Can't move from node not occupied by one of our pieces. ]")
            return State.Invalid

        if self.board.move_to(move.origin, move.to):
            self._did_create_mill = True
            return State.CreatedMill
        self._end_turn()
        return State.Valid

    def _try_remove(self, cmd_remove: Remove, gh: GraphicsHandler) -> State:
        remove = self.board.nodes[cmd_remove.at]
        if remove.color == Color.Empty:
            gh.add_message("   [ Invalid: Can't remove piece from an empty node. ]")
            return State.Invalid
        if remove.color == self.current_player.color:
            gh.add_message("   [ Invalid: Can't remove our own pieces. ]")
            return State.Invalid

        # Is the piece we want to remove part of a mill?
        # If it isn't, it's always a legal move
        if not self.board.is_part_of_mill(cmd_remove.at):
            self.board.remove(cmd_remove.at, self.get_opponent())
            self._end_turn()
            return State.Valid

        # if it is, we need to check if all other pieces of the same color
        # are part of mills, then it's a legal move

        # Loop through all the nodes that are of the same color
        # as the piece we're going to remove, figure out if
        # it's NOT part of a mill. If it isn't, the move is not legal.

        for idx, check in enumerate(self.board.nodes):
            if remove.color != check.color:
                continue

            if not self.board.is_part_of_mill(idx):
                gh.add_message(
                    "   [ Invalid: Can't remove piece from mill when pieces not part of mills exist. ]")
                return State.Invalid

        # We only found pieces that were part of mills, so it's a legal move
        self.board.remove(cmd_remove.at, self.get_opponent())
        self._end_turn()
        return State.Valid

    def get_piece_count(self, color: Color) -> int:
        if color == Color.Black:
            return self.board.num_black
        elif color == Color.White:
            return self.board.num_white
        assert False, "   [ Bug: Unknown color (or empty) ]"

    def update_mills(self) -> bool:
        pass
