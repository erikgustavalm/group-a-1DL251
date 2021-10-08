import pickle
import asyncio
import socket
from asyncio.tasks import sleep
import random
from concurrent.futures import FIRST_COMPLETED
from typing import Tuple

import commands
from color import Color

# TODO set this to something better
MAX_READ_BYTES = 4096


async def handle_new_client_connection(reader, writer, connected, max_players):
    if await is_full(len(connected), max_players):
        writer.write(pickle.dumps(commands.GameIsFull()))
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    writer.write(pickle.dumps(commands.GetName()))
    await writer.drain()
    cmd = pickle.loads(await reader.read(MAX_READ_BYTES))
    if not cmd:
        return

    if isinstance(cmd, commands.SetName):
        connected.append((cmd.name, reader, writer))
    else:
        assert False, f"Invalid command: '{cmd}'"

    # TODO handle duplicate name? here or in client?
    print(f"Connected players: {len(connected)} of {max_players}")


async def run_tournament(connected, max_players):
    while not await is_full(len(connected), max_players):
        # TODO, necessary? will consume lots of CPU if removed
        await asyncio.sleep(0.1)

    # TODO: set up a schedule with the connected players, then pick
    # players from that schedule instead of hardcoding it

    # TODO: use Group L's scoreboard manager here
    scoreboard = None

    # TODO: send scores to everyone?
    # so that even the waiting clients can see something is happening
    # or maybe send the moves to all clients
    # but the clients not currently playing are just in a spectator mode?

    res = await run_match(connected[0], connected[1])
    # if res.game_completed == true:
    #   check winner, add to players score
    #   SEND SCOREBOARD TO ALL PLAYERS
    # else:
    #   remove the disconnected player from the game as if they
    #   had not been in the game in the first place
    # loop back, choose 2 new players, and start a new match etc..
    # exit loop when all players have played against each other


async def run_match(
        p1: Tuple[str, asyncio.StreamReader, asyncio.StreamWriter],
        p2: Tuple[str, asyncio.StreamReader, asyncio.StreamWriter]):
    print("match has started")

    # TODO randomize which player gets which color,
    # or should it be determined by the game schedule?

    cp_name, cp_reader, cp_writer = p1  # current player
    op_name, op_reader, op_writer = p2  # other player

    print(f"Black/player 1 is {cp_name}: {cp_writer.get_extra_info('peername')}")
    print(f"White/player 2 is {op_name}: {op_writer.get_extra_info('peername')}")

    try:
        cp_writer.write(pickle.dumps(commands.StartGame(op_name, Color.Black)))
        await cp_writer.drain()
        op_writer.write(pickle.dumps(commands.StartGame(cp_name, Color.White)))
        await op_writer.drain()

        while True:
            print("reading from both cp_reader and op_reader and getting the first that's done")
            cp_read_task = asyncio.create_task(cp_reader.read(MAX_READ_BYTES))
            op_read_task = asyncio.create_task(op_reader.read(MAX_READ_BYTES))
            done, pending = await asyncio.wait({cp_read_task, op_read_task}, return_when=FIRST_COMPLETED)
            # Cancel all pending tasks
            for task in pending:
                task.cancel()
            if cp_read_task in done:
                cp_response = pickle.loads(cp_read_task.result())
                print(f"(current) cp_read_task done first, val: {cp_response}")
            if op_read_task in done:
                cp_response = pickle.loads(op_read_task.result())
                # swap current and other player since it's the same player as last loop iteration
                cp_name, op_name = op_name, cp_name
                cp_reader, op_reader = op_reader, cp_reader
                cp_writer, op_writer = op_writer, cp_writer
                print(f"(other) op_read_task done first (so switched op and cp), val: {cp_response}")

            # TODO disconnected
            if not cp_response:
                assert False

            if isinstance(cp_response, commands.Lost):
                # TODO handle this
                # ?? Maybe send "lost black" instead?
                # We don't need to send this to the other player,
                # if we've send the same moves to both, one player
                # should win when the other loses.
                # We check .Lost on both, but if it's the networked player,
                # just display that the client won and go back to waiting for a
                # start_game message
                assert False
            elif isinstance(cp_response, commands.Draw):
                # TODO handle this
                assert False

            # debug printing
            addr = cp_writer.get_extra_info('peername')
            print(f"Received {cp_response!a} from {cp_name} {addr!a}")

            # send current player response to other player
            op_writer.write(pickle.dumps(cp_response))
            await op_writer.drain()

            # swap current and other player
            cp_name, op_name = op_name, cp_name
            cp_reader, op_reader = op_reader, cp_reader
            cp_writer, op_writer = op_writer, cp_writer

            #await asyncio.sleep(1.0)

    except ConnectionResetError:
        # Should send "player_disconnected" message
        # or something to the other player, so they can stop waiting
        # (or keep waiting but in a "waiting for a new game" state)
        print("ConnectionResetError (player disconnected?)")
    except ConnectionAbortedError:
        print("ConnectionAbortedError (player disconnected?)")


async def is_full(num_connected, max_players):
    return num_connected >= max_players


def run_server():
    # TODO: Ask host to input max players

    # TODO: Ask host to input number of bot players

    # TODO: handle bot players, just save them in the connected array
    #       so instead of (asyncio.StreamReader, asyncio.StreamWriter),
    #       the connected array could just have contain the bot class
    #       instance then use isinstance to figure out if its a bot.
    #       OR implement a .read and .write function,
    #       that you can call just like StreamReader.read and
    #       StreamWriter.write so just save (Bot, Bot) in the connected array.

    print("Starting tournament (currently 1v1)")

    max_players = 2
    connected = []

    port = input("give port: ")

    print(f"Connected players: {len(connected)} of {max_players}")

    loop = asyncio.get_event_loop()
    loop.create_task(accept_connections(connected, max_players, port))
    loop.create_task(run_tournament(connected, max_players))
    loop.run_forever()


async def accept_connections(connected, max_players, port):
    await asyncio.start_server(lambda r, w: handle_new_client_connection(r, w, connected, max_players), '127.0.0.1', int(port))