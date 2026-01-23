import numpy as np 
from GameEngine.State import State
from colorama import Fore
def input_from_user():
        while True:
            index=input(Fore.WHITE+'Enter the index of the piece you want to move: ')
            try: 
                index=int(index)
                break
            except:
                print(Fore.RED+'Invalid move ,try again')
        return index
class Player:
    
    def choose_move(self, state: State , roll: int = None):
        pass

class HumanPlayer(Player):
    def choose_move(self, state: State , roll: int = None ):
        legal_moves = state.legal_moves()
        move = input_from_user()
        while move not in legal_moves:
            move = input_from_user()
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