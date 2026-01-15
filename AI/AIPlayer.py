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




chance = Chance()
ROLL_PROBS = chance.possible_rolls() 


def effective_pos(pos: int) -> float:
    if pos == 26:
        return 26.5
    if pos == 27:
        return 15.0
    if pos == 28:
        return ROLL_PROBS[3] * 35 + (1 - ROLL_PROBS[3]) * 15
    if pos == 29:
        return ROLL_PROBS[2] * 35 + (1 - ROLL_PROBS[2]) * 15
    if pos == 30:
        return 35.0
    return float(pos)


def evaluate(state) -> float:
    
    own_poss = [i+1 for i in range(30) if state.cells[i].player == 1]
    opp_poss = [i+1 for i in range(30) if state.cells[i].player == 0]

    own_progress = sum(effective_pos(p) for p in own_poss) + 35.0 * state.white_pieces
    opp_progress = sum(effective_pos(p) for p in opp_poss) + 35.0 * state.black_pieces
    progress_score = own_progress - opp_progress

    ai_threat_opp = 0.0
    opp_threat_ai = 0.0

    for o in own_poss:
        for roll in range(1, 6):
            target = o + roll
            if target > 30:
                continue
            if target in opp_poss:
                ai_threat_opp += ROLL_PROBS[roll]

    for o in opp_poss:
        for roll in range(1, 6):
            target = o + roll
            if target > 30:
                continue
            if target in own_poss:
                opp_threat_ai += ROLL_PROBS[roll]

    safety_score = 50.0 * ai_threat_opp - 50.0 * opp_threat_ai

    swap_bonus = 0.0
    if state.last_hit == 1:
        swap_bonus = 20.0
    elif state.last_hit == 0:
        swap_bonus = -20.0

    if state.white_pieces == 7:
        return 10000.0
    if state.black_pieces == 7:
        return -10000.0

    final_value = progress_score + 0.65 * safety_score + swap_bonus
    return final_value
    
