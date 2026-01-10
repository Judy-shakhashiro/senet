"""
This is main file where is an entry point to our project
"""
from GameEngine.State import State
from GameEngine.Rules import Rules
from GameEngine.Chance import Chance
from GameEngine.Player import HumanPlayer
from AI.AIPlayer import AIPlayer
from GameController import GameController

state = State()
rules = Rules()
chance = Chance()

player_max = AIPlayer(depth=3)
player_min = HumanPlayer()

# view = GUIView()

game = GameController(
    state=state,
    rules=rules,
    chance=chance,
    player_max=player_max,
    player_min=player_min,
    # view=view
)

game.game_loop()
