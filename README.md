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

## How to pay the game?
Players can choose to play game **Local** or **Online** in menu, which contains to play with real players or AI bots.
+ Local: 
  1. Play with 1 player
  2. AI bot that you can decide difficulties by Easy, Moderite, Hard
+ Online:
  1. Start a server: Just hold a sever, not playing a game.  Chose "player num", "bot num", "port", then wait for others' connection, if players full then start the round-robin tournment.
  2. Join an existing server: Chose "port" and enter "name" to join the game, waiting for server to start game

## Interface
+ Menu:
<img width="674" alt="螢幕快照 2021-10-27 下午4 47 55" src="https://user-images.githubusercontent.com/50803416/139090194-25e2b08f-aba4-4170-995a-7067b7b095d2.png">

+ Loacl - Play with AI bot:
<img width="477" alt="螢幕快照 2021-10-27 下午4 48 32" src="https://user-images.githubusercontent.com/50803416/139090369-fe15206d-c775-4640-b5d0-7ed9a052d3e3.png">

+ Online - Start a new server:
<img width="654" alt="螢幕快照 2021-10-27 下午4 49 05" src="https://user-images.githubusercontent.com/50803416/139090517-04982b5b-9283-4c7e-9e59-1de603a77a84.png">


+ Board:
<img width="409" alt="螢幕快照 2021-10-27 下午3 56 15" src="https://user-images.githubusercontent.com/50803416/139090220-67b4d381-3af5-40f4-8650-6d9e56b6088b.png">

