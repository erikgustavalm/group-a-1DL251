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
from difficulty import Difficulty
from port import get_port
from typing import Union
from color import Color
from player import Player

START_PIECES = 11
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


def game_init(input_handler: input_handler.InputHandler) -> game_state.GameState:
    # TODO: Change how selecting of match vs AI is done
    # playing a local match
    print("   Please input player name (Within 15 characters):\n"
          "   enter name: easy, medium, hard for AI\n"
          "   ------------------------------------------------")

    p1_name = input_handler.get_input("   Player 1:  ", False)
    if isinstance(p1_name, commands.Quit):
        return commands.Quit()
    p1_name = p1_name[:15]
    
    p2_name = p1_name
    while p2_name == p1_name:
        p2_name = input_handler.get_input("   Player 2:  ", False)
        if isinstance(p2_name, commands.Quit):
            return commands.Quit()
        p2_name = p2_name[:15]
        if p2_name == p1_name:
            print("Can't have the same name as Player 1, try again or type 'q' or 'quit' to return to the menu.")

    num_nodes = len(board_connections)
    player1 = Player(p1_name)
    player2 = Player(p2_name)

    gs = game_state.GameState(player1, player2,
                              (num_nodes, board_connections, mills))
    gs.set_color()
    return gs

def game_bot_init(player1_name, player1_color, bot_name, bot_diff) -> game_state.GameState:
    num_nodes = len(board_connections)
    player1 = Player(player1_name)
    player2 = bot.Bot(bot_name, bot_diff)
    gs = game_state.GameState(player1, player2, (num_nodes, board_connections, mills))
    player2.set_board(gs.board)
    gs.set_color(player1_color)
    return gs

def game_loop(input_handler: input_handler.InputHandler,
              graphics_handler: graphics.GraphicsHandler,
              state: game_state.GameState):
    while True:
        graphics_handler.display_game([node.color for node in state.board.nodes])

        current_state = state.next()
        if current_state == CommandType.Lost:
            graphics_handler.display_winner(state.get_opponent())
            return state.get_opponent().name
        elif current_state == CommandType.Draw:
            graphics_handler.display_draw()
            return commands.Draw()

        graphics_handler.display_status(state.player1, state.player2, state.current_turn, state.current_player)
        graphics_handler.display_messages()

        print(f"   Player {state.current_player.name} ({graphics.color_to_ascii(state.current_player.color)}): It's your turn now ")
        # TODO: may need rework
        if  isinstance(state.current_player, bot.Bot):
            cmd = state.current_player.get_command(current_state, state.current_phase(state.current_player))
        else:
            cmd = input_handler.get_command(current_state)

        if isinstance(cmd, commands.Quit):
            return cmd
        elif isinstance(cmd, commands.Surrender):
            print(f"    {state.current_player.name} ({graphics.color_to_ascii(state.current_player.color)}): surrendered the game!")
            graphics_handler.display_winner(state.get_opponent())
            return cmd

        state.try_command(cmd, graphics_handler)

async def play_local_bot_match(player_name: str,
                               your_color: str,
                               bot_name: str,
                               bot_diff: Difficulty,
                               writer: asyncio.StreamWriter,
                               input_handler: input_handler.InputHandler,
                               graphics_handler: graphics.GraphicsHandler
                               ) -> bool:
    init_state = game_bot_init(player_name, your_color, bot_name, bot_diff)
    res = game_loop(input_handler, graphics_handler, init_state)
    writer.write(pickle.dumps(res))
    await writer.drain()

    return not isinstance(res, commands.Quit)

async def play_networked_match(player_name: str,
                               op_name: str,
                               your_color: str,
                               reader: asyncio.StreamReader,
                               writer: asyncio.StreamWriter,
                               input_handler: input_handler.InputHandler,
                               graphics_handler: graphics.GraphicsHandler
                               ) -> bool:
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
            return True
        elif current_state == CommandType.Draw:
            # Send to server so it knows the match is a draw.
            # only send it from the local player
            if state.current_player == state.player1:
                writer.write(pickle.dumps(commands.Draw()))
                await writer.drain()
                print(f"Sent: {commands.Draw()}")
            graphics_handler.display_draw()
            return True

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
                    writer.write(pickle.dumps(cmd))
                    await writer.drain()
                    return False
                elif isinstance(cmd, commands.Surrender):
                    print(f"    {state.current_player.name} ({graphics.color_to_ascii(state.current_player.color)}): surrendered the game!")
                    graphics_handler.display_winner(state.get_opponent())
                    writer.write(pickle.dumps(cmd))
                    await writer.drain()
                    return True

                res = state.try_command(cmd, graphics_handler)
                graphics_handler.display_messages()

            writer.write(pickle.dumps(cmd))
            await writer.drain()
            print(f"Sent: {cmd}")
        else:
            ### remote player ###
            res = await reader.read(network.MAX_READ_BYTES)
            # print(f"num bytes: {len(res)}")
            cmd = pickle.loads(res)
            # print(cmd)

            ## TODO handle surrender and quit commands
            ## OR should the server translate those commands to something else?
            if isinstance(cmd, commands.Quit):
                print(f"   {state.current_player.name} ({graphics.color_to_ascii(state.current_player.color)}): quit from game!")
                graphics_handler.display_winner(state.get_opponent())
                return True
            elif isinstance(cmd, commands.Surrender):
                print(f"   {state.current_player.name} ({graphics.color_to_ascii(state.current_player.color)}): surrendered the game!")
                graphics_handler.display_winner(state.get_opponent())
                return True
            elif isinstance(cmd, commands.OpponentDisconnected):
                print(f"   {state.current_player.name} ({graphics.color_to_ascii(state.current_player.color)}): disconnected from game!")
                graphics_handler.display_winner(state.get_opponent())
                return True
            elif isinstance(cmd, commands.DisplayScoreboard):
                assert False, "BUG: Shouldn't get a display scoreboard command during a match"
            elif isinstance(cmd, commands.Lost):
                # TODO does this message need to be handled on the client?
                # or is it enough for the server to deal with it?
                # the game state should already know it's over
                assert False, "Not yet implemented"


            print(f"try_command with {cmd}")
            state.try_command(cmd, graphics_handler)
    return True



async def run_networked_game(ih: input_handler.InputHandler, gh: graphics.GraphicsHandler) -> bool:
    # TODO better port handling, don't crash if invalid int
    while True:
        port: Union[int, commands.Quit] = get_port()
        if isinstance(port, commands.Quit):
            # NOTE quitting here returns to the menu,
            # change this to False to actually quit
            return True
        try:
            reader, writer = await asyncio.open_connection('127.0.0.1', port)
            break
        except ConnectionRefusedError as e:
            print("Server refused connection, try again or type 'quit' or 'q' to go back to the menu")

    # writer.transport.set_write_buffer_limits(0, 0)
    print("Connected to tournament.")

    request = None
    op_name = None
    try:
        while True:
            # print("waiting for message")
            res = await reader.read(network.MAX_READ_BYTES)
            # print(f"num bytes: {len(res)}")
            cmd = pickle.loads(res)

            if not cmd:
                print("connection refused")
                writer.close()
                await writer.wait_closed()
                return True

            print("received:", cmd)

            if isinstance(cmd, commands.GetName):
                player_name = ih.get_input("   Your name:  ", False)
                if isinstance(player_name, commands.Quit):
                    return True
                player_name = player_name[:15]

                writer.write(pickle.dumps(commands.SetName(player_name)))
                await writer.drain()
                print("wrote:", commands.SetName(player_name))
            elif isinstance(cmd, commands.StartGame):
                res = await play_networked_match(player_name, cmd.op_name, cmd.your_color, reader, writer, ih, gh)
                if not res:
                    writer.close()
                    await writer.wait_closed()
                    return False
            elif isinstance(cmd, commands.StartBotGame):
                res = await play_local_bot_match(player_name, cmd.your_color, cmd.bot_name, cmd.bot_diff, writer, ih, gh)
                if not res:
                    writer.close()
                    await writer.wait_closed()
                    return False
                # TODO: what is this?
            elif isinstance(cmd, commands.OpponentDisconnected):
                assert False, "Not yet implemented, can this happen outside a match?"
            elif isinstance(cmd, commands.DisplayScoreboard):
                print("DISPLAY SPECTATOR SCOREBOARD (will display the same for all players, even the ones that just finished a match)")
                # TODO: nicer printing of scoreboard
                print(cmd.scoreboard)
            else:
                assert False, f"Unknown command: {cmd}"
        writer.close()
        await writer.wait_closed()
        return True

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

    while True:
        ghandler.display_menu()

        option = ihandler.get_input("   Option([ P / A / S / C / Q ]):  ")
        if isinstance(option, commands.Quit):
            break
        elif option == 'P':
            state = game_init(ihandler)
            if isinstance(state, commands.Quit):
                continue
            game_loop(ihandler, ghandler, state)
        elif option == 'A':
            ghandler.display_AI_menu()
            level = ihandler.get_input("   Option([ E / M / H ]):  ")
            if isinstance(level, commands.Quit):
                continue
            print("   Option = ", level )
        elif option == 'C':
            # Broken on Windows, see https://github.com/aio-libs/aiohttp/issues/4324#issuecomment-733884349 for another "fix"
            # res = asyncio.run(run_networked_game(ihandler, ghandler))
            loop = asyncio.get_event_loop()
            res = loop.run_until_complete(run_networked_game(ihandler, ghandler))
            if not res:
                return
        elif option == 'S':
            ghandler.display_start_tournament()
            network.run_server()
        else:
            print("  Invalid input !\n ")


if __name__ == "__main__":
    main()
