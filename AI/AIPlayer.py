from GameEngine.Chance import Chance
from GameEngine.Player import Player
from GameEngine.State import State
import math

class AIPlayer(Player):
    def __init__(self, chance_model : Chance  ,max_depth: int=3):
        self.max_depth = max_depth
        self.chance_model= chance_model
        
    def pass_turn(self, state: State) :
        child = state.copy()
        if child.current_player == 0:
            child.current_player = 1
        else:
            child.current_player = 0
        child.turnCount += 1
        return child
    
    def expectiminimax(self, state: State, depth: int):
        if depth == 0 or state.is_end():
            return self.evaluate(state)
        
        expected_value=0.0
        for options,weights in self.chance_model.outcomes():
                if state.current_player == 1:
                    v = self.max_node_after_throw(state, options, depth)
                else:
                    v = self.min_node_after_throw(state, options, depth)
                expected_value += weights * v
        return expected_value
    

    # MAX decision after throw
    def max_node_after_throw(self, state: State, options: int, depth: int):
        copy_state=state.copy()
        copy_state.rolled_value=options
        moves = copy_state.legal_moves()
        if not moves:
            child = self.pass_turn(copy_state)
            return self.expectiminimax(child, depth - 1)
        best_value = -math.inf
        for move in moves:
            child = copy_state.copy()
            child.move_piece(move) 
            value = self.expectiminimax(child, depth - 1)
            best_value = max(best_value, value)

        return best_value

    # MIN decision after throw
    def min_node_after_throw(self, state: State, options: int, depth: int):
        copy_state=state.copy()
        copy_state.rolled_value=options
        moves = copy_state.legal_moves()
        if not moves:
            child = self.pass_turn(copy_state)
            return self.expectiminimax(child, depth - 1)
        best_value = math.inf
        for move in moves:
            child = copy_state.copy()
            child.move_piece(move)
            value = self.expectiminimax(child, depth - 1)
            best_value = min(best_value, value)

        return best_value

    def choose_move(self, state: State, options: int):
        copy_state=state.copy()
        copy_state.rolled_value=options
        moves = copy_state.legal_moves()
        if not moves:
            return None

        if state.current_player == 1:  
            best_value = -math.inf
            best_move = None
            for move in moves:
                child = copy_state.copy()
                child.move_piece(move)
                v = self.expectiminimax(child, self.max_depth - 1)
                if v > best_value:
                    best_value = v
                    best_move = move
            return best_move

        else:  
            best_value = math.inf
            best_move = None
            for move in moves:
                child = copy_state.copy()
                child.move_piece(move)
                v = self.expectiminimax(child, self.max_depth - 1)
                if v < best_value:
                    best_value = v
                    best_move = move
            return best_move


    def evaluate(self, state: State) -> float:
        winner = state.winner_player
        if winner == "white":
            return 10000
        if winner == "black":
            return -10000
        return 0.0
    
