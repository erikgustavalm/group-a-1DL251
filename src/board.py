from __future__ import annotations

from dataclasses import dataclass
from color import Color
from player import Player


@dataclass
class Node:
    adjacents: [int]
    color: Color


def _create_possible_mills(num_intersections: int, mills: [[int]]) -> dict[int, [[int]]]:
    possible_mills = {}
    for i in range(num_intersections + 1):
        possible_mills[i] = []
    for mill in mills:
        possible_mills[mill[0]].append([mill[1], mill[2]])
        possible_mills[mill[1]].append([mill[0], mill[2]])
        possible_mills[mill[2]].append([mill[0], mill[1]])
    return possible_mills


@dataclass
class Board:
    nodes: [Node]
    possible_mills: dict[int, [[int]]]

    def __init__(self, nodes: int, adjacent: [[int]], mills: [[int]]):
        self.nodes = []
        for idx in range(nodes):
            self.nodes.append(Node(adjacent[idx], Color.Empty))

        self.possible_mills = _create_possible_mills(nodes, mills)

    def is_part_of_mill(self, node_idx: int) -> bool:
        for mills in self.possible_mills[node_idx]:
            for other in mills:
                if self.nodes[node_idx].color != self.nodes[other].color:
                    break
            else:
                return True
        return False

    def remove(self, node_idx: int, remove_from: Player):
        self.nodes[node_idx].color = Color.Empty
        remove_from.pieces -= 1

    # returns: if placing the piece created a mill
    def place(self, to: int, player: Player) -> bool:
        self.nodes[to].color = player.color
        player.coins_left_to_place -= 1
        player.pieces += 1
        return self.is_part_of_mill(to)

    # returns: if the move created a mill or not
    def move_to(self, origin: int, to: int) -> bool:
        self.nodes[to].color = self.nodes[origin].color
        self.nodes[origin].color = Color.Empty
        return self.is_part_of_mill(to)

    def get_nodes(self, player: Player):
        node_indexes = []
        for idx, node in enumerate(self.nodes):
            if node.color == player.color:
                node_indexes.append(idx)
        return node_indexes
