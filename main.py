import os
import random

import graphics
import input_handler
import game_state

from color import Color

def main():

    Input = input_handler.InputHandler()
    gh = graphics.GraphicsHandler()
    
    game_start = True
    while game_start:
    	gh.display_menu()
    	
    	menu_option = Input.get_input("   Option([ P / E ]):  ")
    	option = menu_option[0].upper()
    	
    	if option[0] == 'E':
	        while game_start:
        		sure_exit = Input.get_input("   Sure to exit([ Y / N ]):  ")
        		sure_exit = sure_exit[0].upper()
        		
        		if sure_exit == 'Y':
        			print("\n   >>> Exit Game\n")
        			game_start = False
        		elif sure_exit == 'N':
        			os.system('clear')
        			break
        		else:
        			print("   Invalid input !\n")
        			continue 
    	elif option[0] == 'P':
        	os.system('clear')
	        
	        state = game_state.GameState()
	        
	        print("   Please input player name (Ｗithin 15 words):\n"
                  "   -------------------------------------------")
	        p1_name = Input.get_input("   Player 1:  ")
	        p2_name = Input.get_input("   Player 2:  ")

	        # Decide who is black (Do we need to write a function?)
	        random.seed('foobar')
	        seq = [ 1, 2 ]
	        if random.choice(seq) == '1':
	        	p_black = game_state.Player(str(p1_name), Color.Black, 11)
	        	p_white = game_state.Player(p2_name[0], Color.White, 11)
	        else:
	        	p_black = game_state.Player(p2_name[0], Color.Black, 11)
	        	p_white = game_state.Player(p1_name[0], Color.White, 11)
            
	        game_is_running = True
	        while game_is_running:
	        	# gh.display_status()
	        	# Title
		        print("  ╔═════════════════════════════════════════════════════════════════════════════════════════════╗\n"
		              "  ║                                           UU-Game                                           ║\n"
		              "  ╚═════════════════════════════════════════════════════════════════════════════════════════════╝\n")
		        
		        print("   Round %d ( remaining turns: %d )" %(state.current_turn, 250-state.current_turn))
		        print("  ┌───────────────────────┬────────────────────┐\n"
		        	  "  │ %-15s( ██ ) │   %2d pieces left   │\n"
		        	  "  ├───────────────────────┼────────────────────┤\n"
		        	  "  │ %-15s( ░░ ) │   %2d pieces left   │\n" 
		        	  "  └───────────────────────┴────────────────────┘\n" %(p_black.name, p_black.coins_left_to_place, p_white.name, p_white.coins_left_to_place))
		        gh.display_game([Color.White, Color.Black, Color.Empty] * 8)

		        # Command action
                # Rules
                
		        state.current_turn += 1
                # end_game situation
		        game_is_running = False          
		        game_start = False
    	else:
	        print("  Invalid input !\n ")
	        continue
    

if __name__ == "__main__":
    main()
