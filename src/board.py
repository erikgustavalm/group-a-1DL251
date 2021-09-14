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
        for i in range(num_intersections+1):
            self.possible_mills[i] = []
        for mill in mills:
            self.possible_mills[mill[0]].append([mill[1], mill[2]])
            self.possible_mills[mill[1]].append([mill[0], mill[2]])
            self.possible_mills[mill[2]].append([mill[0], mill[1]])

    # returns if the move created a mill or not
    def move_to(self, origin: int, to: int) -> bool:
        nodes[to].change_to(nodes[origin].color)
        nodes[origin].change_to(Color.Empty)

        for possible_mill in possible_mills[nodes[to]]:
            for node in possible_mill:
                if nodes[to].color != node.color:
                    break
            else:
                return True

        return False

@dataclass
class Node:
    adjacents: [Node]
    color: Color

    def change_to(self, color: Color):
        self.color = color
