from typing import List
from color import Color

from player import Player


def color_to_ascii(c: Color):
    if c == Color.Black:
        return "██"
    elif c == Color.White:
        return "▒▒"
    else:
        return "  "

def display_small_title(self):
    print("   ╔═════════════════════════════════════════════════════╗\n"
          "   ║                       UU-Game                       ║\n"
          "   ╚═════════════════════════════════════════════════════╝\n ")

def display_tournament(self):
    print("  ╔══════════════════════════════════════════════════════════════════════════════════════════╗\n"
          "  ║                                        Tournament                                        ║\n"
          "  ╚══════════════════════════════════════════════════════════════════════════════════════════╝\n\n")
    
def display_big_title(self):
    # Game title
    print("  ╔═════════════════════════════════════════════════════════════════════════════════════════╗\n"
          "  ║                                         UU-Game                                         ║\n"
          "  ╚═════════════════════════════════════════════════════════════════════════════════════════╝\n")    

class GraphicsHandler:
    _messages: [str] = []

    def add_message(self, message: str):
        self._messages.append(message)

    
    def display_menu(self):
        display_big_title(self)
        print("      >>>                                   M E N U                                  <<<\n\n"
              "      ─────────────    Local    ─────────────     ─────────────    Online   ─────────────\n\n"
              "      ┌─────────────────────────────────────┐     ┌─────────────────────────────────────┐\n"
              "      │        Player  vs  Player [P]       │     │        Start New Tournament [S]     │\n"
              "      └─────────────────────────────────────┘     └─────────────────────────────────────┘\n"
              "      ┌─────────────────────────────────────┐     ┌─────────────────────────────────────┐\n" 
              "      │        Player  vs    AI   [A]       │     │  Connect to Existing Tournament [C] │\n"
              "      └─────────────────────────────────────┘     └─────────────────────────────────────┘\n\n\n"
              "      ────────────────────────────────────  Quit [Q]  ────────────────────────────────────\n\n")
  
    def display_AI_menu(self):
        display_small_title(self)
        print("    >>>                   AI Level                   <<<\n\n"
              "    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐\n"
              "    │   Easy [E]   │  │ Moderate [M] │  │   Hard [H]   │\n"
              "    └──────────────┘  └──────────────┘  └──────────────┘\n\n\n"
              "    ───────────────   Back to Menu [B]   ───────────────\n\n")
    
    def display_start_tournament(self):
        display_tournament(self)
        print("      >>>                         Total Player Number: 3 ~ 8                         <<< \n\n"
              "       ┌───                                                                           \n"
              "       │         If [ Number of Real Players ] < [ Total Number of Players ],         \n"
              "                               AI Bot will be used as a substitute                   │\n"
              "                                                                                  ───┘\n\n"
              "      ─────────────────────────────────  Please Input  ─────────────────────────────────\n")
        
    def display_status(self, player1: Player, player2: Player, current_turn, current_player: Player):
        if current_player.color == player1.color:
            p1_turn = " ──>"; p2_turn = "    "
        else:
            p1_turn = "    "; p2_turn = " ──>"
        
        # Player status
        print("   Round %d ( Remaining turns: %d )" %(current_turn, 250-current_turn))
        
        print("        ┌───────────────────────┬────────────────────┐\n"
              "  %s  │ %-15s( %s ) │   %2d pieces left   │\n"
              "        ├───────────────────────┼────────────────────┤\n"
              "  %s  │ %-15s( %s ) │   %2d pieces left   │\n"
              "        └───────────────────────┴────────────────────┘\n" % (p1_turn, player1.name, color_to_ascii(player1.color), player1.coins_left_to_place, p2_turn, player2.name, color_to_ascii(player2.color), player2.coins_left_to_place))

    def display_game(self, board: [Color]):
        # NOTE: Modifies board variable destructively (contents change outside function)
        for idx, c in enumerate(board):
            board[idx] = color_to_ascii(c)

        print("    ┌─────┐                 ┌─────┐                 ┌─────┐\n"
              "    │1  {}├─────────────────┤2  {}├─────────────────┤3  {}│\n"
              "    └──┬──┘                 └──┬──┘                 └──┬──┘\n"
              "       │   \                   │                  /    │\n"
              "       │    ┌─────┐         ┌──┴──┐         ┌─────┐    │\n"
              "       │    │4  {}├─────────┤5  {}├─────────┤6  {}│    │\n"
              "       │    └──┬──┘         └──┬──┘         └──┬──┘    │\n"
              "       │       │               │               │       │\n"
              "       │       │    ┌─────┐ ┌──┴──┐ ┌─────┐    │       │\n"
              "       │       │    │7  {}├─┤8  {}│-│9  {}│    │       │\n"
              "       │       │    └──┬──┘ └─────┘ └──┬──┘    │       │\n"
              "       │       │       │               │       │       │\n"
              "    ┌──┴──┐ ┌──┴──┐ ┌──┴──┐         ┌──┴──┐ ┌──┴──┐ ┌──┴──┐\n"
              "    │10 {}├─┤11 {}├─┤12 {}│         │13 {}├─┤14 {}├─┤15 {}│\n"
              "    └──┬──┘ └──┬──┘ └──┬──┘         └──┬──┘ └──┬──┘ └──┬──┘\n"
              "       │       │       │               │       │       │\n"
              "       │       │    ┌──┴──┐ ┌─────┐ ┌──┴──┐    │       │\n"
              "       │       │    │16 {}├─┤17 {}├─┤18 {}│    │       │\n"
              "       │       │    └─────┘ └──┬──┘ └─────┘    │       │\n"
              "       │       │               │               │       │\n"
              "       │    ┌──┴──┐         ┌──┴──┐         ┌──┴──┐    │\n"
              "       │    │19 {}├─────────┤20 {}├─────────┤21 {}│    │\n"
              "       │    └─────┘         └──┬──┘         └─────┘    │\n"
              "       │   /                   │                   \   │\n"
              "    ┌──┴──┐                 ┌──┴──┐                 ┌──┴──┐\n"
              "    │22 {}├─────────────────┤23 {}├─────────────────┤24 {}│\n"
              "    └─────┘                 └─────┘                 └─────┘\n".format(
                  board[0], board[1], board[2],
                  board[3], board[4], board[5],
                  board[6], board[7], board[8],
                  board[9], board[10], board[11],
                  board[12], board[13], board[14],
                  board[15], board[16], board[17],
                  board[18], board[19], board[20],
                  board[21], board[22], board[23]))

    def display_messages(self):
        for message in self._messages:
            print(message)
        self._messages = []

    def display_winner(self, player: Player):
        print("               ^ _______________________________________________ ^\n"
              "              /                                                   \\\n"
              "             │                                                     │\n"
              "             │       %-15s ( %s ) has won the game~      │ \n"
              "             │                                                     │\n"
              "             │                                                     │\n"
              "             └─────────────────────────────────────────────────────┘\n"
              "               (\n"
              "               )\n"
              "      .^___^. (\n"
              "     (´. w .`)n\n"
              "     o　　 c /\n"
              "     0__ . /                                       Design by Group A\n"
              "       .( /     *   *   *   *   *   *   *   *   *   *   *   *   *   *\n"
              "\n" % ( player.name, color_to_ascii(player.color) ) )

    
    def display_draw(self):
        print("             º──────────────────────────────────┐\n"
              "             │                                  │\n"
              "             │             D R A W              │\n"
              "             │                                  │\n"
              "             │──────────────────────────────────┘\n"
              "    ^____^   │\n"
              "   ( . w . ) │\n"
              "   <　     >０\n"
              "    │     │\n"
              "    U ─── U\n")