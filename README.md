# Group A


## Introduction of game

### Game Rules: 
The UU-GAME is a two-player board game designed to be played in the terminal by two players on the same device using the keyboard. The goal of the game is to eliminate all but two of your opponents pieces by creating mills.

Before starting the game, the players will be assigned the colors black and white. This color determines which color of pieces they will be playing. When the game starts, each player has 11 pieces of their color. The player who is assigned the black color will begin the game.

The game can be divided into three main phases: 
  1. The players take turns placing their pieces on the intersections of the board. There can only be one piece at a time on each of the intersections. When a player has placed all 11 pieces, the player will move into the second phase. 
  2. The players will take turns moving their pieces. A piece can only be moved to unoccupied adjacent intersections connected by lines. If a player cannot move any of their pieces, that player will automatically lose the game. A player moves from phase 2 to phase 3 when the player only has 3 pieces left on the board.  
  3. The player can move their pieces to any unoccupied intersection on the board. The player is only allowed to move one piece per round during all three phases. 

During any of these three phases, the players can create mills. Creating a mill means having three adjacent pieces in a row that are connected by lines. If one of the players makes a mill, they will be allowed to remove one of their opponent pieces. They are only allowed to remove a piece from one of the opponent’s mills if no other pieces are available. 

There are four cases in which the game can end: 
  1. If one of the players only has two pieces left on the board, this makes the other player the winner. 
  2. If the game exceeds a total of 250 turns, in this case the game will end in a draw. 
  3. If a player cannot move any of their pieces in phase 2, in this case that player will lose. 
  4. The game can end with one of the players surrendering, quitting, exiting which leaves the other player as the winner.


## Dependencies
+ python version: 3.9

## How to play the game?
Players can choose to play game **Local** or **Online** in menu, which contains to play with real players or AI bots.
+ Local: 
  1. Play with 1 player
  2. AI bot that you can decide difficulties by Easy, Moderate, Hard
+ Online:
  1. Start a server: Just hold a sever, not playing a game.  Chose "player num", "bot num", "port", then wait for others' connection, if players full then start the round-robin tournment.
  2. Join an existing server: Chose "port" and enter "name" to join the game, waiting for server to start game

## Interface
### Menu:
<img width="664" alt="螢幕快照 2021-10-27 下午5 21 37" src="https://user-images.githubusercontent.com/50803416/139099485-a92aa480-26a8-418f-9ac8-fb520faded9a.png">


### Loacl - Play with AI bot:
<img width="491" alt="螢幕快照 2021-10-27 下午5 22 00" src="https://user-images.githubusercontent.com/50803416/139099525-ffbb7b4e-3d83-4221-bae2-aed121bbe46b.png">


### Online - Start a new server:
<img width="888" alt="螢幕快照 2021-10-27 下午5 37 43" src="https://user-images.githubusercontent.com/50803416/139099602-ee3afa89-02bb-42df-be5b-2edf25d8aad1.png">

  #### ScoreBoard: <img width="510" alt="螢幕快照 2021-10-27 下午5 39 07" src="https://user-images.githubusercontent.com/50803416/139099851-bfc21e10-51b4-4974-8d65-4993631e4dd7.png">
  #### Tournment end: <img width="449" alt="螢幕快照 2021-10-27 下午5 39 19" src="https://user-images.githubusercontent.com/50803416/139099996-91e317dc-0c14-435a-b02b-b1262e1b519d.png">


### Board:
<img width="444" alt="螢幕快照 2021-10-27 下午5 21 11" src="https://user-images.githubusercontent.com/50803416/139099616-5b5995df-5fd7-47d9-a467-91d26a1d0c6e.png">


