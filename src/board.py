from __future__ import annotations

from dataclasses import dataclass
from color import Color


@dataclass
class Board:
    nodes: [Node]
    possible_mills: dict[int, [[int]]]
    num_black: int
    num_white: int

    def __create_possible_mills(self, num_intersections: int, mills: [[int]]):
        self.possible_mills = {}
        for i in range(num_intersections + 1):
            self.possible_mills[i] = []
        for mill in mills:
            self.possible_mills[mill[0]].append([mill[1], mill[2]])
            self.possible_mills[mill[1]].append([mill[0], mill[2]])
            self.possible_mills[mill[2]].append([mill[0], mill[1]])

    def is_part_of_mill(self, node_idx: int) -> bool:
        for possible_mill in self.board.possible_mills[node_idx]:
            for other in possible_mill:
                if nodes[node_idx].color != nodes[other].color:
                    break
            else:
                return True
        return False

    def replace(self, node_idx: int, new_color: Color):
        if nodes[node_idx].color == Color.Black:
            num_black -= 1
        elif nodes[node_idx].color == Color.White:
            num_white -= 1
        nodes[node_idx].color = new_color

    def remove(self, node_idx: int):
        replace(node_idx, Color.Empty)

    # returns: if placing the piece created a mill
    def place(self, to, color) -> bool:
        replace(to, color)
        return is_part_of_mill(nodes[to])

    # returns: if the move created a mill or not
    def move_to(self, origin: int, to: int) -> bool:
        replace(to, nodes[origin].color)
        remove(origin)
        return is_part_of_mill(nodes[to])


@dataclass
class Node:
    adjacents: [Node]
    color: Color
