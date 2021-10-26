import random
from commands import CommandType, Command, Surrender, Place, Move, Remove
from color import Color
from phase import Phase
from enum import Enum, auto
from board import Board
from player import Player
from difficulty import Difficulty

class Bot(Player):
    diff = None
    board = None
    opposite_color = None

    def __init__(self, name: str, difficulty = Difficulty.Easy):
        super().__init__(name)
        self.diff = difficulty

    def set_board(self, board: Board):
        self.board = board

    def _skip_false(node, adj, rating, mod):
        if node == 0 and adj == 3:
            return rating
        if node == 2 and adj == 5:
            return rating
        if node == 22 and adj == 18:
            return rating
        if node == 23 and adj == 20:
            return rating

        return rating + mod

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
                        rating = self._skip_false(node.idx, adj, rating, 1)

            # Give rating if the placing will destroy opponents adjacents
            for other in self.board.get_nodes(self.opposite_color):
                for adj in other.adjacents:
                    if adj is node.idx:
                        rating = self._skip_false(node.idx, adj, rating, 1)

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

    def _possible_removes(self) -> [int]:
        pos_removes = []
        others = self.board.get_nodes_of_color(self.opposite_color)
        for node in others:
            if not self.board.potential_is_part_of_mill(node, self.opposite_color):
                pos_removes.append(node)
        if len(pos_removes) > 0:
            return pos_removes
        return others

    def _best_remove(self) -> Command:
        pos_removes = self._possible_removes()
        best_remove = [(0, pos_removes[0].idx)]

        for node in pos_removes:
            rating = 0
            # Give rating for removing close to own pieces
            for other in self.board.get_nodes_of_color(self.color):
                for adj in node.adjacents:
                    if adj is other:
                        rating = self._skip_false(node.idx, adj, rating, 1)

            # Give rating if the placing will destroy opponents adjacents
            for other in self.board.get_nodes(self.opposite_color):
                for adj in other.adjacents:
                    if adj is node.idx:
                        rating = self._skip_false(node.idx, adj, rating, 1)

            # Give rating for destroying oponents mill
            if self.board.potential_is_part_of_mill(node.idx, self.opposite_color):
                rating = rating + 5

            if best_remove[0][0] < rating:
                best_remove = [(rating, node.idx)]
            elif best_remove[0][0] == rating:
                best_remove.append((rating, node.idx))

        return Remove(random.choice(best_remove)[1])

    def _remove_cmd(self) -> Command:
        pos_removes = self._possible_removes()
        if self.diff == Difficulty.Easy:
            return Remove(random.choice(pos_removes))
        elif self.diff == Difficulty.Medium:
            return Remove(random.choice(pos_removes))
        elif self.diff == Difficulty.Hard:
            return Remove(random.choice(pos_removes))

    def _possible_moves(self, color) -> [(int, int)]:
        # Returns all the possible moves that a player can do
        pos_moves = []
        for node in self.board.get_nodes(color):
            for other in self.board.get_nodes_of_color(Color.Empty):
                for adj in node.adjacents:
                    if adj is other:
                        pos_moves.append((node.idx, other))
        return pos_moves

    def _best_move(self) -> Command:
        pos_moves = self._possible_moves(self.color)

        # Surrender if no move is possible
        if len(pos_moves) == 0:
            return Surrender()

        best_move = [(0, pos_moves[0])]
        for node_from, node_to in pos_moves:
            rating = 0

            for other in self.board.get_nodes_of_color(self.color):
                # Give points to moving close to others of same color
                for adj in self.board.nodes[node_to].adjacents:
                    if other is adj:
                        rating = self._skip_false(node_to, adj, rating, 1)

                # Reduce points for moving away from others of same color
                for adj in self.board.nodes[node_from].adjacents:
                    if other is adj:
                        rating = self._skip_false(node_from, adj, rating, -1)


            for other in self.board.get_nodes_of_color(self.opposite_color):
                # Give points for blocking opponent
                for adj in self.board.nodes[node_to].adjacents:
                    if other is adj:
                        rating = self._skip_false(node_to, adj, rating, 1)

                # Reduce points if stop blocking opponent
                for adj in self.board.nodes[node_from].adjacents:
                    if other is adj:
                        rating = self._skip_false(node_from, adj, rating, -1)

            # Give rating for creating mill
            if self.board.potential_is_part_of_mill(node_to, self.color):
                rating = rating + 5

            # Give rating for destroying oponents mill
            if self.board.potential_is_part_of_mill(node_to, self.opposite_color):
                rating = rating + 5

            if best_move[0][0] < rating:
                best_move = [(rating, (node_from, node_to))]
            elif best_move[0][0] == rating:
                best_move.append((rating, (node_from, node_to)))

        final_node_from, final_node_to = random.choice(best_move)[1]

        return Move(final_node_from, final_node_to)

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
            return self._best_move()

    def _possible_teleports(self) -> [(int, int)]:
        pos_teles = []
        for node in self.board.get_nodes_of_color(self.color):
            for other in self.board.get_nodes_of_color(Color.Empty):
                pos_teles.append((node, other))
        return pos_teles

    def _best_teleport(self) -> Command:
        pos_tele = self._possible_teleports()
        best_tele = [(0, pos_tele[0])]
        for node_from, node_to in pos_tele:
            rating = 0

            for other in self.board.get_nodes_of_color(self.color):
                # Give points to moving close to others of same color
                for adj in self.board.nodes[node_to].adjacents:
                    if other is adj:
                        rating = self._skip_false(node_to, adj, rating, 1)

                # Reduce points for moving away from others of same color
                for adj in self.board.nodes[node_from].adjacents:
                    if other is adj:
                        rating = self._skip_false(node_from, adj, rating, -1)

            for other in self.board.get_nodes_of_color(self.opposite_color):
                # Give points for blocking opponent
                for adj in self.board.nodes[node_to].adjacents:
                    if other is adj:
                        rating = self._skip_false(node_to, adj, rating, 1)

                # Reduce points if stop blocking opponent
                for adj in self.board.nodes[node_from].adjacents:
                    if other is adj:
                        rating = self._skip_false(node_from, adj, rating, -1)

            # Give rating for creating mill
            if self.board.potential_is_part_of_mill(node_to, self.color):
                rating = rating + 5

            # Give rating for destroying oponents mill
            if self.board.potential_is_part_of_mill(node_to, self.opposite_color):
                rating = rating + 5

            if best_tele[0][0] < rating:
                best_tele = [(rating, (node_from, node_to))]
            elif best_tele[0][0] == rating:
                best_tele.append((rating, (node_from, node_to)))

        final_node_from, final_node_to = random.choice(best_tele)[1]

        return Move(final_node_from, final_node_to)


    def _teleport_cmd(self) -> Command:
        if self.diff == Difficulty.Easy:
            pos_teles = self._possible_teleports()
            if len(pos_teles) > 0:
                node_from, node_to = random.choice(pos_teles)
                return Move(node_from, node_to)
            return Surrender()
        elif self.diff == Difficulty.Medium:
            pos_teles = self._possible_teleports()
            if len(pos_teles) > 0:
                node_from, node_to = random.choice(pos_teles)
                return Move(node_from, node_to)
            return Surrender()
        elif self.diff == Difficulty.Hard:
            return self._best_teleport()


    def get_command(self, cmd: CommandType, curr_phase: Phase) -> Command:
        self.opposite_color = Color.Black if self.color == Color.White else Color.White

        if cmd == CommandType.Remove:
            return self._remove_cmd()
        elif curr_phase == Phase.One:
            return self._place_cmd()
        elif curr_phase == Phase.Two:
            return self._move_cmd()
        elif curr_phase == Phase.Three:
            return self._teleport_cmd()
