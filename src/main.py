import os
import random

import graphics
import input_handler
import game_state
from game_state import NextState
import commands

from color import Color
from state import State

board_connections = list({
    1: [2, 4, 10],
    2: [1, 3, 5],
    3: [2, 15, 6],
    4: [1, 5, 11],
    5: [4, 2, 6, 8],
    6: [3, 5, 14],
    7: [12, 8],
    8: [7, 5, 9],
    9: [8, 13],
    10: [1, 11, 22],
    11: [4, 10, 12, 19],
    12: [11, 7, 16],
    13: [9, 14, 18],
    14: [13, 6, 15, 21],
    15: [14, 3, 24],
    16: [12, 17],
    17: [16, 18, 20],
    18: [13, 17],
    19: [11, 20, 22],
    20: [19, 17, 21, 23],
    21: [14, 20, 24],
    22: [10, 19, 23],
    23: [22, 20, 24],
    24: [23, 21, 15],
}.values())
board_connections = [[x - 1 for x in l] for l in board_connections]

mills = [
    # horizontal
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
    [13, 14, 15],
    [16, 17, 18],
    [19, 20, 21],
    [22, 23, 24],
    # vertical
    [1, 10, 22],
    [4, 11, 19],
    [7, 12, 16],
    [2, 5, 8],
    [17, 20, 23],
    [9, 13, 18],
    [6, 14, 21],
    [3, 15, 24]
]
mills = [[x - 1 for x in l] for l in mills]


def clear():
    return
    # if os.name == "posix":  # linux or mac
    #     os.system('clear')
    # elif os.name == "nt":  # windows
    #     os.system('cls')


def main():
    # vt100 escape codes test, if "Test" is printed in blue it works
    # os.system(" ")
    # print('\033[36mTest\033[0m')
    # return

    # TODO move the loop into an event loop class/function
    # so it's easier for others to integrate our code with theirs

    Input = input_handler.InputHandler()
    gh = graphics.GraphicsHandler()

    game_start = True
    while game_start:
        gh.display_menu()

        option = Input.get_input("   Option([ P / E ]):  ")

        if option == 'E':
            while game_start:
                sure_exit = Input.get_input("   Sure to exit([ Y / N ]):  ")
                if sure_exit == 'Y':
                    print("\n   >>> Exit Game\n")
                    game_start = False
                elif sure_exit == 'N':
                    clear()
                    break
                else:
                    print("   Invalid input !\n")
                    continue
        elif option == 'P':
            clear()
            print("   Please input player name (Ｗithin 15 words):\n"
                  "   -------------------------------------------")
            # TODO check that the input is not empty, retry until non-empty
            # TODO (?) check that p1_name is not the same as p2_name, retry until different
            p1_name = Input.get_input("   Player 1:  ")
            p2_name = Input.get_input("   Player 2:  ")

            num_nodes = len(board_connections)
            state = game_state.GameState(
                p1_name, p2_name, (num_nodes, board_connections, mills))

            game_is_running = True
            while game_is_running:
                gh.display_status(
                    state.player1, state.player2, state.current_turn)
                gh.display_game([node.color for node in state.board.nodes])
                gh.display_messages()

                player_str = f"   Player {state.current_player.name}:  "

                next = state.next()
                if next == NextState.Place:
                    response = Input.get_input(
                        player_str + f"[place piece at] ")

                    # TODO handle surrender (or quit?) command

                    # TODO validate the response (better)
                    if not response.isdigit():
                        continue
                    to = int(response) - 1
                    if not (0 <= to < num_nodes):
                        continue

                    cmd = commands.Place(to)
                    state.try_command(cmd, gh)
                elif next == NextState.Remove:
                    response = Input.get_input(
                        player_str + f"[node to remove] ")

                    # TODO validate the response (better)
                    if not response.isdigit():
                        continue
                    at = int(response) - 1
                    if not (0 <= at < num_nodes):
                        continue

                    cmd = commands.RemoveAfterMill(at)
                    state.try_command(cmd, gh)
                elif next == NextState.Move:
                    response = Input.get_separated_input(
                        player_str + f"[from] [to] ")

                    # TODO validate the response (better)
                    if len(response) != 2:
                        continue
                    if not response[0].isdigit() or not response[1].isdigit():
                        continue
                    origin = int(response[0]) - 1
                    to = int(response[1]) - 1
                    if not (0 <= origin < num_nodes and 0 <= to < num_nodes):
                        continue

                    cmd = commands.Move(origin, to)
                    state.try_command(cmd, gh)

                elif next == NextState.Lost:
                    print(f"Player {state.get_opponent().name} won!")
                    game_is_running = False
                else:
                    assert False, "Unhandled state"
        else:
            print("  Invalid input !\n ")
            continue


if __name__ == "__main__":
    main()
