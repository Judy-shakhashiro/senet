import numpy as np 
from GameEngine.State import State
from colorama import Fore
class Player:
    def choose_move(self, state: State , roll: int = None):
        pass

class HumanPlayer(Player):
    def choose_move(self, state: State , roll: int = None ):
        legal_moves = state.legal_moves()
        move = int(input(Fore.WHITE + "Enter index to move :"))
        while move not in legal_moves:
            move = int(input("Invalid, try again: "))
        return move

class RandomPlayer(Player):
    def choose_move(self, state: State , roll: int = None):
        legal_moves = state.legal_moves()

        if not legal_moves :
            return None
        
        chosen = np.random.choice(legal_moves )
        return chosen


class LastPawnPlayer(Player):
    
    def choose_move(self, state: State , roll: int = None):
        legal_moves = state.legal_moves()
        
        if not legal_moves:
            return None
        
        chosen = np.max(legal_moves)
        return chosen