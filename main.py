"""
This is main file where is an entry point to our project
"""
from GameEngine.State import State
from GameEngine.Chance import Chance
from AI.AIPlayer import AIPlayer
from GameController import GameController
from colorama import Fore, Back, Style
from GameEngine.Player import (
    HumanPlayer,
    RandomPlayer,
    LastPawnPlayer
)

def main():
    state = State()
    chance = Chance()
    depth = int(input(Fore.WHITE + "Enter deptth you wanna to play with:"))
    debug = input("Show AI debug info? (y/n): ").strip().lower() == "y"
    player1 = AIPlayer(chance_model=chance,max_depth = depth,debug=debug)
    
    player2 = RandomPlayer()
    state.play_two_players(player1 , player2,chance,debug=debug)
    # state.play_two_players(player1 , player2,chance)


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
