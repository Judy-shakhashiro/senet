"""
This is main file where is an entry point to our project
"""
import math
from GameEngine.State import State
from GameEngine.Chance import Chance
from GameEngine.Player import RandomPlayer , LastPawnPlayer , HumanPlayer
from AI.AIPlayer import AIPlayer

from colorama import Fore, Back, Style
def main():
    state = State()
    chance = Chance()
    depth = int(input(Fore.WHITE + "Enter deptth you wanna to play with:"))
    debug = input("Show AI debug info? (y/n): ").strip().lower() == "y"
    palyer1 = AIPlayer(chance_model=chance,max_depth = depth,debug=debug)
    # player2 = AIPlayer(chance_model=chance,max_depth = depth,debug=debug)
    player2 = LastPawnPlayer()
     
    state.play_two_players(palyer1, player2 , chance , debug=debug)


    # state.play_ai_vs_human(ai_player,debug=debug)
    # depth = int(input("Enter depth: "))
    # ai_player = AIPlayer(chance_model=chance, max_depth=depth)
    # move = ai_player.choose_move(state, options=1)
    # print("WITHOUT USING ALPHA/BETA:")
    # print("Move chosen:", move)
    # print("Nodes expanded:", ai_player.last_choice_nodes)
    # print("Time:", ai_player.last_choice_time)
    # print("Eval:", ai_player.last_choice_value)
    
    
    
    # player_max = AIPlayer(chance_model=chance,max_depth=4)
    # player_min = HumanPlayer()

    # view = GUIView()

    # game = GameController(
    #     state=state,
    #     chance=chance,
    #     player_max=player_max,
    #     player_min=player_min,
    #     # view=view
    # )

    # game.game_loop()
    # state.play()
    
if __name__ == "__main__":
    main()    
