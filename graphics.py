from color import Color

from game_state import Player
from game_state import GameState

from dataclasses import dataclass


@dataclass
class GraphicsHandler:
    def display_menu(self):
        print("   ╔═════════════════════╗\n"
              "   ║       UU-Game       ║\n"
              "   ╚═════════════════════╝\n ")

        print("       >    MENU    < \n\n"
              "       -   Play [P] \n"
              "       -   Exit [E] \n")
    def display_status(self, ):
        # Title
        print("  ╔═════════════════════════════════════════════════════════════════════════════════════════════╗\n"
              "  ║                                           UU-Game                                           ║\n"
              "  ╚═════════════════════════════════════════════════════════════════════════════════════════════╝\n")
        # Round
        print("   Round %d ( remaining turns: %d ) \n" %(current_turn, 250-current_turn))
        # Player status


    def display_game(self, board: [Color]):
        # NOTE: Modifies board variable destructively (contents change outside function)

        for idx, c in enumerate(board):
            if c == Color.Black:
                board[idx] = "██"
            elif c == Color.White:
                board[idx] = "░░"
            else:
                board[idx] = "  "

        print("    ┌─────┐                 ┌─────┐                 ┌─────┐\n"
              "     1  {} ───────────────── 2  {} ───────────────── 3  {} \n"
              "    └─────┘                 └─────┘                 └─────┘\n"
              "       │   \                   │                  /    │\n"
              "       │    ┌─────┐         ┌─────┐         ┌─────┐    │\n"
              "       │     4  {} ───────── 5  {} ───────── 6  {}     │\n"
              "       │    └─────┘         └─────┘         └─────┘    │\n"
              "       │       │               │               │       │\n"
              "       │       │    ┌─────┐ ┌─────┐ ┌─────┐    │       │\n"
              "       │       │     7  {} ─ 8  {} - 9  {}     │       │\n"
              "       │       │    └─────┘ └─────┘ └─────┘    │       │\n"
              "       │       │       │               │       │       │\n"
              "    ┌─────┐ ┌─────┐ ┌─────┐         ┌─────┐ ┌─────┐ ┌─────┐\n"
              "     10 {} ─ 11 {} ─ 12 {}           13 {} ─ 14 {} ─ 15 {}\n"
              "    └─────┘ └─────┘ └─────┘         └─────┘ └─────┘ └─────┘\n"
              "       │       │       │               │       │       │\n"
              "       │       │    ┌─────┐ ┌─────┐ ┌─────┐    │       │\n"
              "       │       │     16 {} ─ 17 {} ─ 18 {}     │       │\n"
              "       │       │    └─────┘ └─────┘ └─────┘    │       │\n"
              "       │       │               │               │       │\n"
              "       │    ┌─────┐         ┌─────┐         ┌─────┐    │\n"
              "       │     19 {} ───────── 20 {} ───────── 21 {}     │\n"
              "       │    └─────┘         └─────┘         └─────┘    │\n"
              "       │   /                   │                   \   │\n"
              "    ┌─────┐                 ┌─────┐                 ┌─────┐\n"
              "     22 {} ───────────────── 23 {} ───────────────── 24 {}\n"
              "    └─────┘                 └─────┘                 └─────┘\n".format(
                board[0], board[1], board[2],
                board[3], board[4], board[5],
                board[6], board[7], board[8],
                board[9], board[10], board[11],
                board[12], board[13], board[14],
                board[15], board[16], board[17],
                board[18], board[19], board[20],
                board[21], board[22], board[23]))
        """
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
                board[21], board[22], board[23]))"""

    def display_winner(self, player: Player):
        print(
            "-----------------------------------------\n"
            "|                                       |\n"
            "|   {} has won the game!          |\n"
            "|                                       |\n"
            "|          Play again? y/n              |\n"
            "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n".format(player.name))
