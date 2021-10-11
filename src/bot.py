import random
from commands import CommandType, Command, Surrender, Place, Move, Remove
#from game_state import GameState
from color import Color
from phase import Phase
from enum import Enum, auto
from board import Board
from player import Player

# TODO don't just randomly pick a move that might be invalid, check phase
#      and if in phase 2, check adjacents so it doesn't pick a move that's invalid.
# TODO Add three bot difficulty levels
    # Moderate: completely random, just like currently (except no invalid moves)
    # Easy: Pick a random move that will avoid creating a mill unless forced to
    # Hard: Loop through the possible mills, check if the opponent is about to
    #       create a mill and if so, block it. Otherwise, make a move that would
    #       create a mill for us (or build towards one)

# NOTE: doesn't need to be a class currently. Might never need to be a class?
class Difficulty(Enum):
    Easy = auto()
    Medium = auto()
    Hard = auto()

_bot_names = ["hAIkon", "mAIchel", "helenAI", "sarAI"]

class Bot(Player):
    diff = None
    board = None
    opposite_color = None

    def __init__(self, board: Board, color, start_coins, difficulty = Difficulty.Easy):
        super().__init__(random.choice(_bot_names) + f"[{difficulty.name}]", color, start_coins)
        self.diff = difficulty
        self.board = board

    def _possible_moves(self, color) -> [(int, int)]:
        # Returns all the possible moves that a player can do
        pos_moves = []
        for node in self.board.get_nodes(color):
            for other in self.board.get_nodes_of_color(Color.Empty):
                for adj in node.adjacents:
                    if adj is other:
                        pos_moves.append((adj, other))

        return pos_moves

    def _best_place(self) -> Command:
        # Rate the placings, so we can find the best
        pos_place = self.board.get_nodes(Color.Empty)
        rated_place = [(0, pos_place[0].idx)]

        for node in pos_place:
            rating = 0
            # Give rating for placing close to own pieces
            for other in self.board.get_nodes_of_color(self.color):
                for adj in node.adjacents:
                    if adj is other:
                        rating = rating + 1

            # Give rating if the placing will destroy opponents adjacents
            for other in self.board.get_nodes(self.opposite_color):
                for adj in other.adjacents:
                    if adj is node.idx:
                        rating = rating + 1

            # Give rating for creating mill
            if self.board.potential_is_part_of_mill(node.idx, self.color):
                rating = rating + 5

            # Give rating for destroying oponents mill
            if self.board.potential_is_part_of_mill(node.idx, self.opposite_color):
                rating = rating + 5

            if rated_place[0][0] < rating:
                rated_place = [(rating, node.idx)]
            elif rated_place[0][0] == rating:
                rated_place.append((rating, node.idx))

        return Place(random.choice(rated_place)[1])

    def _best_move(self) -> Command:
        pos_moves = self._possible_moves(self.color)
        best_move = [(0, pos_moves[0])]
        for node_from, node_to in pos_moves:
            rating = 0

            for other in self.board.get_nodes_of_color(self.color):
                # Give points to moving close to others of same color
                for adj in self.board.nodes[node_to].adjacents:
                    if other is adj:
                        rating = rating + 1

                # Reduce points for moving away from others of same color
                for adj in self.board.nodes[node_from].adjacents:
                    if other is adj:
                        rating = rating - 1



        pass

    def _possible_teleports(self) -> [(int, int)]:
        pos_teles = []
        for node in self.board.get_nodes(self.color):
            for other in self.board.get_nodes_of_color(Color.Empty):
                pos_teles.append((node, other))
        return pos_teles


    def _possible_removes(self) -> [int]:
        pos_removes = []
        others = self.board.get_nodes_of_color(self.opposite_color)
        for node in others:
            if not self.board.potential_is_part_of_mill(node, self.opposite_color):
                pos_removes.append(node)
        if len(pos_removes) > 0:
            return pos_removes
        return others


    def _place_cmd(self) -> Command:
         if self.diff == Difficulty.Easy:
             return Place(random.choice(self.board.get_nodes_of_color(Color.Empty)))
         elif self.diff == Difficulty.Medium:
             pos_place = self._possible_moves(self.color)
             if len(pos_place) > 0:
                 _, pos_to = random.choice(pos_place)
                 return Place(pos_to)
             pos_place = self._possible_moves(self.opposite_color)
             if len(pos_place) > 0:
                 _, pos_to = random.choice(pos_place)
                 return Place(pos_to)
             return Place(random.choice(self.board.get_nodes_of_color(Color.Empty)))
         elif self.diff == Difficulty.Hard:
             return self._best_place()


    def _remove_cmd(self) -> Command:
        pos_removes = self._possible_removes()
        if self.diff == Difficulty.Easy:
            return Remove(random.choice(pos_removes))
        elif self.diff == Difficulty.Medium:
            return Remove(random.choice(pos_removes))
        elif self.diff == Difficulty.Hard:
            return Remove(random.choice(pos_removes))


    def _move_cmd(self) -> Command:
        pos_moves = self._possible_moves(self.color)
        if self.diff == Difficulty.Easy:
            if len(pos_moves) > 0:
                node_from, node_to = random.choice(pos_moves)
                return Move(node_from, node_to)
            return Surrender()
        elif self.diff == Difficulty.Medium:
            if len(pos_moves) > 0:
                node_from, node_to = random.choice(pos_moves)
                return Move(node_from, node_to)
            return Surrender()
        elif self.diff == Difficulty.Hard:
            self._best_move()


    def _teleport_cmd(self, empty: [int], placed: [int]) -> Command:
        if self.diff == Difficulty.Easy:
            pos_teles = self._possible_teleports()
            if len(pos_teles) > 0:
                node_from, node_to = random.choice(pos_teles)
                return Move(node_from, node_to)
            return Surrender()
        elif self.diff == Difficulty.Medium:
            pass
        elif self.diff == Difficulty.Hard:
            pass


    def get_command(self, cmd: CommandType, curr_phase: Phase) -> Command:
        # nodes_our = state.board.get_player_nodes(state.current_player)
        # nodes_their = state.board.get_player_nodes(state.get_opponent())
        # nodes_empty = state.board.get_nodes_of_color(Color.Empty)
        # curr_phase = state.current_phase()

        self.opposite_color = Color.Black if self.color == Color.White else Color.White
        # TODO (?) Let bot choose to surrender in some cases?


        if cmd == CommandType.Remove:
            return self._remove_cmd()
        elif curr_phase == Phase.One:
            return self._place_cmd()
        elif curr_phase == Phase.Two:
            return self._move_cmd()
        elif curr_phase == Phase.Three:
            return self._teleport_cmd()

        # if False:
        #     return Surrender()
        # if cmd == CommandType.Place:
        #     return Place(random.choice(nodes_empty))
        # elif cmd == CommandType.Move:
        #     return Move(random.choice(nodes_our), random.choice(nodes_empty))
        # elif cmd == CommandType.Remove:
        #     return Remove(random.choice(nodes_their))
