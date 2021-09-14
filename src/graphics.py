from color import Color
from dataclasses import dataclass
from game_state import Player


@dataclass
class GraphicsHandler:
    def display_game(self, board: [Color]):
        # NOTE: Modifies board variable destructively (contents change outside function)
        for idx, c in enumerate(board):
            if c == Color.Black:
                board[idx] = "■"
            elif c == Color.White:
                board[idx] = "o"
            else:
                board[idx] = " "

        print(
            "[{}]1────────────────[{}]2────────────────[{}]3\n"
            " │   \               │               /   │\n"
            " │     [{}]4─────────[{}]5─────────[{}]6    │\n"
            " │      │            │            │      │\n"
            " │      │     [{}]7──[{}]8──[{}]9    │      │\n"
            " │      │      │           │      │      │\n"
            "[{}]10──[{}]11──[{}]12       [{}]13──[{}]14──[{}]15\n"
            " │      │      │           │      │      │\n"
            " │      │     [{}]16─[{}]17─[{}]18   │      │\n"
            " │      │            │            │      │\n"
            " │     [{}]19────────[{}]20────────[{}]21   │\n"
            " │   /               │               \   │\n"
            "[{}]22───────────────[{}]23───────────────[{}]24\n".format(
                board[0], board[1], board[2],
                board[3], board[4], board[5],
                board[6], board[7], board[8],
                board[9], board[10], board[11],
                board[12], board[13], board[14],
                board[15], board[16], board[17],
                board[18], board[19], board[20],
                board[21], board[22], board[23]))

    def display_winner(self, player: Player):
        print(
            "-----------------------------------------\n"
            "|                                       |\n"
            "|   {} has won the game!          |\n"
            "|                                       |\n"
            "|          Play again? y/n              |\n"
            "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n".format(player.name))
