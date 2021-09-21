from color import Color

from game_state import Player
from game_state import GameState

from dataclasses import dataclass

def color_to_ascii(c: Color):
    if c == Color.Black:
        return "██"
    elif c == Color.White:
        return "▒▒"
    else:
        return "  "


@dataclass
class GraphicsHandler:
    def display_menu(self):
        print("   ╔═════════════════════╗\n"
              "   ║       UU-Game       ║\n"
              "   ╚═════════════════════╝\n ")

        print("       >    MENU    < \n\n"
              "       -   Play [P] \n"
              "       -   Exit [E] \n")
    def display_status(self, gs: GameState):
        # Game title
        print("  ╔═════════════════════════════════════════════════════════════════════════════════════════════╗\n"
              "  ║                                           UU-Game                                           ║\n"
              "  ╚═════════════════════════════════════════════════════════════════════════════════════════════╝\n")
        # Player status        
        print("   Round %d ( remaining turns: %d )" %(gs.current_turn, 250-gs.current_turn))
        print("  ┌───────────────────────┬────────────────────┐\n"
              "  │ %-15s( %s ) │   %2d pieces left   │\n"
              "  ├───────────────────────┼────────────────────┤\n"
              "  │ %-15s( %s ) │   %2d pieces left   │\n" 
              "  └───────────────────────┴────────────────────┘\n" %(gs.player1.name, color_to_ascii(gs.player1.color), gs.player1.coins_left_to_place, gs.player2.name, color_to_ascii(gs.player2.color), gs.player2.coins_left_to_place))

    def display_game(self, board: [Color]):
        # NOTE: Modifies board variable destructively (contents change outside function)

        for idx, c in enumerate(board):
            board[idx] = color_to_ascii(c)

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


    def display_winner(self, player: Player):
        print(
            "-----------------------------------------\n"
            "|                                       |\n"
            "|   {} has won the game!          |\n"
            "|                                       |\n"
            "|          Play again? y/n              |\n"
            "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n".format(player.name))
