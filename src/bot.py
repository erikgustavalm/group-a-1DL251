import random
from commands import CommandType, Command, Surrender, Quit, Place, Move, Remove
from game_state import GameState
from color import Color

# TODO don't just randomly pick a move that might be invalid, check phase
#      and if in phase 2, check adjacents so it doesn't pick a move that's invalid.
# TODO Add three bot difficulty levels
    # Moderate: completely random, just like currently (except no invalid moves)
    # Easy: Pick a random move that will avoid creating a mill unless forced to
    # Hard: Loop through the possible mills, check if the opponent is about to
    #       create a mill and if so, block it. Otherwise, make a move that would
    #       create a mill for us (or build towards one)

# NOTE: doesn't need to be a class currently. Might never need to be a class?
class Bot():
    def get_command(self, cmd: CommandType, state: GameState) -> Command:
        nodes_our = state.board.get_player_nodes(state.current_player)
        nodes_their = state.board.get_player_nodes(state.get_opponent())
        nodes_empty = state.board.get_nodes_of_color(Color.Empty)

        # TODO (?) Let bot choose to surrender in some cases?
        if False:
            return Surrender()
        if cmd == CommandType.Place:
            return Place(random.choice(nodes_empty))
        elif cmd == CommandType.Move:
            return Move(random.choice(nodes_our), random.choice(nodes_empty))
        elif cmd == CommandType.Remove:
            return Remove(random.choice(nodes_their))
