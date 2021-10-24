import pickle
import asyncio
import socket
from asyncio.tasks import sleep
import random
from concurrent.futures import FIRST_COMPLETED
from typing import List, Optional, Tuple
from enum import Enum, auto
from itertools import combinations

import commands
from color import Color
from scoreboard import Scoreboard
from port import get_port
import os
import errno

class TournamentEnded(Exception):
    pass

# TODO set this to something better
MAX_READ_BYTES = 4096

class MatchResult(Enum):
    Winner = auto()
    Draw = auto()
    Disconnected = auto()

Player = Tuple[str, asyncio.StreamReader, asyncio.StreamWriter]
Match = Tuple[Tuple[Player, Player], int]

def get_player_ident(p: Player):
    (_,_,writer) = p
    return writer.get_extra_info('peername')

async def send_game_full(writer: asyncio.StreamWriter):
    writer.write(pickle.dumps(commands.GameIsFull()))
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def handle_new_client_connection(reader: asyncio.StreamReader,
                                       writer: asyncio.StreamWriter,
                                       connected: List[Player],
                                       max_players: int):
    if is_full(len(connected), max_players):
        send_game_full(writer)
        return
    while True:
        writer.write(pickle.dumps(commands.GetName()))
        await writer.drain()
        cmd = pickle.loads(await reader.read(MAX_READ_BYTES))
        if not cmd:
            return


        if isinstance(cmd, commands.SetName):
            names = [name for (name, _, _) in connected]
            if cmd.name in names:
                continue
            elif is_full(len(connected), max_players):
                send_game_full(writer)
                return
            connected.append((cmd.name, reader, writer))
            break
        else:
            assert False, f"Invalid command: '{cmd}'"

    # TODO handle duplicate name? here or in client?
    print(f"Connected players: {len(connected)} of {max_players}")
'''
async def send_scoreboard_to_all(connected: List[Player], scoreboard: Scoreboard):
    for (_,_, writer) in connected:
        encoded_scoreboardV = commands.DisplayScoreboard(scoreboard.to_encode())
        writer.write(pickle.dumps(encoded_scoreboard))
'''

async def send_scoreboard_to_all(connected: List[Player], match_list: List[Match]):
    scoreboard = {}
    for (player_name, _, _) in connected:
        scoreboard[player_name] = 0 
    for (((p1_name, _, _), (p2_name, _, _)), outcome) in match_list:
        if (outcome == 1):
            scoreboard[p1_name] += 3
        elif (outcome == 2):
            scoreboard[p2_name] += 3
        elif (outcome == 0):
            scoreboard[p1_name] += 1
            scoreboard[p2_name] += 1
    # TODO Make a fancy scoreboard and send it instead of the dictionary
    for (_, _, writer) in connected:
        writer.write(pickle.dumps(scoreboard))

        



def next_match(match_list : List[Match]) -> Optional[Tuple[int, Match]]:
    for idx, match in enumerate(match_list):
        if (match[1] is None):
            return (idx, match)
    return None

#Create a list of matches to be played
#Each match is a tuple which contains a tuple of the players and the outcome
#Outcome is None if match hasn't been played, 1 if player1 won, 2 if player2 won
def create_and_shuffle_matches(connected : List[Player]) -> List[Match]:
    match_list = (
        list(zip(combinations(connected, 2), [None]*len(connected)))
    )
    random.shuffle(match_list)
    return match_list

def handle_disconnect(player_to_remove : Player, match_list : List[Match], connected : List[Player]):
    connected.remove(player_to_remove)

    indexes_to_remove = []
    for idx, match in enumerate(match_list):
        players, _ = match
        if player_to_remove in players:
            indexes_to_remove.append(idx)
    for idx in indexes_to_remove:
        del match_list[idx]

async def run_tournament(connected: List[Player], max_players: int):
    try:
        while not is_full(len(connected), max_players):
            # TODO, necessary? will consume lots of CPU if removed
            await asyncio.sleep(0.1)

        match_list = create_and_shuffle_matches(connected)
        

        # TODO: set up a schedule with the connected players, then pick
        # players from that schedule instead of hardcoding it

        # using Group L's scoreboard manager here
        scoreboard = Scoreboard()

        # TODO: maybe send the moves to all clients, where the clients not 
        # currently playing are in a spectator mode?

        # TODO only loop while there are still matches left to be played
        while True:
            # choose 2 new players from the schedule
            print(len(match_list))
            current_match : Optional[Tuple[int, Match]] = next_match(match_list)
            if (current_match is None):
                print("No more matches to be played!\n")
                break
            print(current_match[1][0][0], current_match[1][0][1])
            (match_index, ((player1, player2), _)) = current_match

            (res, data) = await run_match(player1, player2)

            if res == MatchResult.Winner:
                if data == player1:
                    # player 1 won, add to their score
                    match_list[match_index] = ((player1, player2), 1)
                    # scoreboard.add_score(get_player_ident(player1), get_player_ident(player2))
                elif data == player2:
                    match_list[match_index] = ((player1, player2), 2)
                    # player 2 won, add to their score
                    # scoreboard.add_score(get_player_ident(player2), get_player_ident(player1))
                else:
                    assert False, f"Unknown value: {data}"
                await send_scoreboard_to_all(connected, scoreboard)
            elif res == MatchResult.Draw: # data is None
                # add to both players' score
                match_list[match_index] = ((player1, player2), 0)
                #scoreboard.add_draw(get_player_ident(player1), get_player_ident(player2))
                await send_scoreboard_to_all(connected, scoreboard)
            elif res == MatchResult.Disconnected:
                handle_disconnect(data, match_list, connected)
                # TODO move the exception handling for disconnections
                # to run_tournament from run_match?

                # remove the disconnected player from the game as if they
                # had not been in the game in the first place
                print("Player " + data[0] + " disconnected!\n")
                # assert False, "TODO"
            else:
                assert False, f"Unknown value: {res}"

        raise TournamentEnded
        # assert False, "all players should have played against each other here"

    except KeyboardInterrupt as e:
        print(f"{type(e).__name__}, {e}")
        for (_, _, writer) in connected:
            writer.close()
            await writer.wait_closed()


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

                # TODO should this be cp_* instead of op_*?
                # return the winner
                return MatchResult.Winner, (op_name, op_reader, op_writer)
            elif isinstance(cp_response, commands.Surrender):
                # TODO should this be op_* instead of cp_* and vice versa?
                op_writer.write(pickle.dumps(commands.Surrender()))
                await op_writer.drain()
                return MatchResult.Winner, (op_name, op_reader, op_writer)
            elif isinstance(cp_response, commands.Draw):
                # False if the match ended in a draw.
                return MatchResult.Draw, None
            elif isinstance(cp_response, commands.Quit):
                return MatchResult.Disconnected, (cp_name, cp_reader, cp_writer)

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

    except (EOFError, ConnectionResetError, ConnectionAbortedError) as e:
        # Should send "player_disconnected" message
        # or something to the other player, so they can stop waiting
        # (or keep waiting but in a "waiting for a new game" state)
        # TODO return that the match was invalid and which player disconnected
        # so the score can be cleaned up (both here and for ConnectionAbortedError)
        # can you combine except
        print(f"{type(e).__name__}, {e} (player disconnected?) {repr(e)}")
        _, p1_reader, p1_writer = p1
        _, p2_reader, p2_writer = p2
        if p1_reader.at_eof:
            p1_writer.write(pickle.dumps(commands.OpponentDisconnected()))
            await p1_writer.drain()
            return MatchResult.Disconnected, p1
        elif p2_reader.at_eof:
            p2_writer.write(pickle.dumps(commands.OpponentDisconnected()))
            await p2_writer.drain()
            return MatchResult.Disconnected, p2
        else:
            assert False, "one of the players are not at EOF (is that OK for Connection*Error?)"


def is_full(num_connected: int, max_players: int) -> bool:
    return num_connected >= max_players

server = None

def custom_exception_handler(loop, context):
    global server
    exception = context.get('exception')
    if isinstance(exception, TournamentEnded):
        print("custom_exception_handler TournamentEnded")
        # print(context)
        if server:
            print("called server.close()")
            server.close()
        loop.stop()
        return
    # NOTE not calling this silences exceptions, I think
    loop.default_exception_handler(context)

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

    max_players: int = 3
    connected: List[Player] = []

    loop = asyncio.get_event_loop()
    loop.set_exception_handler(custom_exception_handler)

    loop.create_task(accept_connections(connected, max_players))
    loop.create_task(run_tournament(connected, max_players))

    loop.run_forever()


async def accept_connections(connected: List[Player], max_players: int):
    global server
    while True:
        port: Union[int, commands.Quit] = get_port()
        if isinstance(port, commands.Quit):
            raise TournamentEnded
        try:
            server = await asyncio.start_server(lambda r, w: handle_new_client_connection(r, w, connected, max_players), '127.0.0.1', port)
            print(f"Connected players: {len(connected)} of {max_players}")
            break
        except OSError as e:
            # TODO: 'raise e from e' re-raises the exception,
            # keeping the old stack trace, should we use that instead?
            if (os.name == 'nt' and e.errno != errno.WSAEADDRINUSE
                or os.name == 'posix' and e.errno != errno.EADDRINUSE
                    or os.name not in ['posix', 'nt']):
                raise
            print("Port already in use, try again or type 'quit' or 'q' to go back to the menu")
