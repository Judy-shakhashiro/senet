"""
This is main file where is an entry point to our project
"""
from GameEngine.State import State

from GameEngine.Chance import Chance
from GameEngine.Player import HumanPlayer
from AI.AIPlayer import AIPlayer


state = State()

chance = Chance()

player_max = AIPlayer(chance_model=chance,max_depth=4)
player_min = HumanPlayer()


# game.game_loop()
# state.play()
state.play_ai_vs_human(player_max)
