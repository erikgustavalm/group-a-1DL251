import asyncio
import random
import pickle

import graphics
import input_handler
import game_state
import commands
import bot
from commands import CommandType
import network
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


def game_loop(input_handler: input_handler.InputHandler, graphics_handler: graphics.GraphicsHandler):
    print("   Please input player name (Ｗithin 15 characters):\n"
          "   enter name: easy, medium, hard for AI\n"
          "   ------------------------------------------------")

    p1_name = input_handler.get_input("   Player 1:  ", False)[:15]
    p2_name = p1_name
    while p2_name == p1_name:
        p2_name = input_handler.get_input("   Player 2:  ", False)[:15]
        if p2_name == p1_name:
            print("Can't have the same name as Player 1")

    num_nodes = len(board_connections)
    state = game_state.GameState(p1_name, p2_name,
                                 (num_nodes, board_connections, mills))

    while True:
        graphics_handler.display_game([node.color for node in state.board.nodes])

        current_state = state.next()
        if current_state == CommandType.Lost:
            graphics_handler.display_winner(state.get_opponent())
            return
        elif current_state == CommandType.Draw:
            graphics_handler.display_draw()
            return

        graphics_handler.display_status(state.player1, state.player2, state.current_turn, state.current_player)
        graphics_handler.display_messages()

        print(f"   Player {state.current_player.name} ({graphics.color_to_ascii(state.current_player.color)}): It's your turn now ")
        # TODO: may need rework
        if  isinstance(state.current_player, bot.Bot):
            cmd = state.current_player.get_command(current_state, state.current_phase(state.current_player))
        else:
            cmd = input_handler.get_command(current_state)

        if isinstance(cmd, commands.Quit):
            return
        elif isinstance(cmd, commands.Surrender):
            print(f"    {state.current_player.name} ({graphics.color_to_ascii(state.current_player.color)}): surrendered the game!")
            graphics_handler.display_winner(state.get_opponent())
            return

        state.try_command(cmd, graphics_handler)


async def play_networked_match(player_name: str,
                               op_name: str,
                               your_color: str,
                               reader: asyncio.StreamReader,
                               writer: asyncio.StreamWriter,
                               input_handler: input_handler.InputHandler,
                               graphics_handler: graphics.GraphicsHandler):
    num_nodes = len(board_connections)
    state = game_state.GameState(player_name, op_name,
                                 (num_nodes, board_connections, mills),
                                 your_color)
    while True:
        graphics_handler.display_game([node.color for node in state.board.nodes])

        current_state = state.next()
        if current_state == CommandType.Lost:
            # Send to server so it knows the match is done.
            # Only send if it's the current player who lost,
            # don't need to send for the networked opponent
            if state.current_player == state.player1:
                writer.write(pickle.dumps(commands.Lost()))
                await writer.drain()
                print(f"Sent: {commands.Lost()}")
            graphics_handler.display_winner(state.get_opponent())
            return
        elif current_state == CommandType.Draw:
            # Send to server so it knows the match is a draw.
            # only send it from the local player
            if state.current_player == state.player1:
                writer.write(pickle.dumps(commands.Draw()))
                await writer.drain()
                print(f"Sent: {commands.Draw()}")
            graphics_handler.display_draw()
            return

        graphics_handler.display_status(state.player1, state.player2, state.current_turn, state.current_player)
        graphics_handler.display_messages()

        if state.current_player == state.player1:
            ### local player ###
            print(f"   Player {state.current_player.name} ({graphics.color_to_ascii(state.current_player.color)}): It's your turn now ")
            res = State.Invalid
            while res == State.Invalid:
                cmd = input_handler.get_command(current_state)
                
                # TODO handling of Quit and Surrender is duplicated
                if isinstance(cmd, commands.Quit):
                    assert False, "Not yet implemented"
                elif isinstance(cmd, commands.Surrender):
                    print(f"   {state.current_player.name} ({graphics.color_to_ascii(state.current_player.color)}): surrendered the game!")
                    assert False, "Not yet implemented"

                res = state.try_command(cmd, graphics_handler)
                graphics_handler.display_messages()

            writer.write(pickle.dumps(cmd))
            await writer.drain()
            print(f"Sent: {cmd}")
        else:
            ### remote player ###
            cmd = pickle.loads(await reader.read(network.MAX_READ_BYTES))
        
            ## TODO handle surrender and quit commands
            ## OR should the server translate those commands to something else?
            if isinstance(cmd, commands.Quit):
                assert False, "Not yet implemented"
            elif isinstance(cmd, commands.Surrender):
                print(f"   {state.current_player.name} ({graphics.color_to_ascii(state.current_player.color)}): surrendered the game!")
                assert False, "Not yet implemented"
            elif isinstance(cmd, commands.OpponentDisconnected):
                # just print a "opponent disconnected" message and return?
                assert False, "Not yet implemented"
            elif isinstance(cmd, commands.DisplayScoreboard):
                assert False, "BUG: Shouldn't get a display scoreboard command during a match"
            elif isinstance(cmd, commands.Lost):
                # TODO does this message need to be handled on the client?
                # or is it enough for the server to deal with it?
                # the game state should already know it's over
                assert False, "Not yet implemented"


            print(f"try_command with {cmd}")
            state.try_command(cmd, graphics_handler)



async def run_networked_game(ih: input_handler.InputHandler, gh: graphics.GraphicsHandler):
    # TODO better port handling, don't crash if invalid int
    port = input("server port: ")
    reader, writer = await asyncio.open_connection('127.0.0.1', int(port))
    # writer.transport.set_write_buffer_limits(0, 0)
    print("Connected to tournament.")

    player_name = ih.get_input("   Your name:  ", False)[:15]

    request = None
    op_name = None
    try:
        while True:
            cmd = pickle.loads(await reader.read(network.MAX_READ_BYTES))

            if not cmd:
                print("connection refused")
                writer.close()
                await writer.wait_closed()
                return

            print("received:", cmd)

            if isinstance(cmd, commands.GetName):
                writer.write(pickle.dumps(commands.SetName(player_name)))
                await writer.drain()
                print("wrote:", commands.SetName(player_name))
            elif isinstance(cmd, commands.StartGame):
                await play_networked_match(player_name, cmd.op_name, cmd.your_color, reader, writer, ih, gh)
            elif isinstance(cmd, commands.OpponentDisconnected):
                assert False, "Not yet implemented, can this happen outside a match?"
            elif isinstance(cmd, commands.DisplayScoreboard):
                print("DISPLAY SPECTATOR SCOREBOARD (will display the same for all players, even the ones that just finished a match)")
                # TODO: nicer printing of scoreboard
                print(cmd.scoreboard)
            else:
                assert False, f"Unknown command: {cmd}"

    except KeyboardInterrupt:
        writer.close()
        await writer.wait_closed()
    except ConnectionResetError:
        print("ConnectionResetError (server was shut down?)")
    except ConnectionAbortedError:
        print("ConnectionAbortedError (server was shut down?), can this happen on the client? it can happen on the server")


def main():
    ihandler = input_handler.InputHandler()
    ghandler = graphics.GraphicsHandler()

    game_start = True
    while game_start:
        ghandler.display_menu()

        option = ihandler.get_input("   Option([ P / A / S / C / Q ]):  ")
        if option == 'Q':
            while game_start:
                sure_exit = ihandler.get_input("   Sure to quit([ Y / N ]):  ")
                if sure_exit == 'Y':
                    print("\n   >>> Quit Game\n")
                    game_start = False
                elif sure_exit == 'N':
                    break
                else:
                    print("   Invalid input !\n")
                    continue
        elif option == 'P':
            game_loop(ihandler, ghandler)
        elif option == 'A':
            ghandler.display_AI_menu()
            level = ihandler.get_input("   Option([ E / M / H / B ]):  ")
            print("   Option = ", level )
        elif option == 'C':
            asyncio.run(run_networked_game(ihandler, ghandler))
        elif option == 'S':
            ghandler.display_start_tournament()
            network.run_server()
        else:
            print("  Invalid input !\n ")


if __name__ == "__main__":
    main()
