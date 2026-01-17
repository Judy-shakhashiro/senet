from GameEngine.Chance import Chance
from GameEngine.Player import Player
from GameEngine.State import State
import math
import time

class AIPlayer(Player):
    def __init__(self, chance_model : Chance  ,max_depth: int=4,debug:bool=False):
        self.max_depth = max_depth
        self.chance_model= chance_model
        self.debug=debug
        self.nodes_expanded=0
        self.last_choice_value=None
        self.last_choice_eval=None
        self.last_choice_nodes=0
        self.last_choice_time=0.0
    def reset_states(self):
        self.nodes_expanded=0
        self.last_choice_value=None
        self.last_choice_eval=None
        self.last_choice_nodes=0
        self.last_choice_time=0.0
            
        
    def pass_turn(self, state: State) :
        child = state.copy()
        if child.current_player == 0:
            child.current_player = 1
        else:
            child.current_player = 0
        child.turnCount += 1
        return child
    
    def expectiminimax(self, state: State, depth: int,alpha : float = -math.inf,beta:float=math.inf):
        self.nodes_expanded+=1
        if depth == 0 or state.is_end():
            return evaluate(state)
        
        expected_value=0.0
        for options,weights in self.chance_model.outcomes():
                if state.current_player == 1:
                    v = self.max_node_after_throw(state, options, depth,alpha,beta)
                else:
                    v = self.min_node_after_throw(state, options, depth,alpha,beta)
                expected_value += weights * v
        return expected_value
    

    # MAX decision after throw
    def max_node_after_throw(self, state: State, options: int, depth: int ,alpha:float,beta:float):
        copy_state=state.copy()
        copy_state.rolled_value=options
        moves = copy_state.legal_moves()
        if not moves:
            child = self.pass_turn(copy_state)
            return self.expectiminimax(child, depth - 1 ,alpha,beta)
        def move_sorted(move):
            temp_child = copy_state.copy()
            temp_child.move_piece(move)
            return evaluate(temp_child)
        moves = sorted(moves,key=move_sorted,reverse=True)
        best_value = -math.inf
        for move in moves:
            child = copy_state.copy()
            child.move_piece(move) 
            value = self.expectiminimax(child, depth - 1,alpha,beta)
            best_value = max(best_value, value)
            alpha = max(alpha,best_value)
            if alpha >=beta:
                break

        return best_value

    # MIN decision after throw
    def min_node_after_throw(self, state: State, options: int, depth: int,alpha:float,beta:float):
        copy_state=state.copy()
        copy_state.rolled_value=options
        moves = copy_state.legal_moves()
        if not moves:
            child = self.pass_turn(copy_state)
            return self.expectiminimax(child, depth - 1,alpha,beta)
        def moves_sorted(move):
            temp_child = copy_state.copy()
            temp_child.move_piece(move)
            return evaluate(temp_child)
        moves = sorted(moves,key=moves_sorted)
        best_value = math.inf
        for move in moves:
            child = copy_state.copy()
            child.move_piece(move)
            value = self.expectiminimax(child, depth - 1,alpha,beta)
            best_value = min(best_value, value)
            beta = min(beta,best_value)
            if alpha>=beta:
                break

        return best_value

    def choose_move(self, state: State, options: int):
        self.reset_states()
        copy_state=state.copy()
        copy_state.rolled_value=options
        moves = copy_state.legal_moves()
        time_limit=5.0
        start_time = time.time()
        if not moves:
            self.last_choice_nodes=0
            self.last_choice_time=time.time() - start_time
            self.last_choice_value=None
            return None
        
        if state.current_player == 1:  
            best_value = -math.inf
            best_move = None
            best_eval = None
            for move in moves:
                child = copy_state.copy()
                child.move_piece(move)
                evaluate_state=evaluate(child)
                v = self.expectiminimax(child, self.max_depth - 1, alpha=-math.inf, beta=math.inf)
                if v > best_value:
                    best_value = v
                    best_move = move
                    best_eval = evaluate_state 
                if time.time() - start_time > time_limit:
                    break   
            self.last_choice_value=best_value
            self.last_choice_eval = best_eval
            self.last_choice_nodes=self.nodes_expanded
            self.last_choice_time=time.time() - start_time  
            return best_move

        else:  
            best_value = math.inf
            best_move = None
            for move in moves:
                child = copy_state.copy()
                child.move_piece(move)
                v = self.expectiminimax(child, self.max_depth - 1, alpha=-math.inf, beta=math.inf)
                if v < best_value:
                    best_value = v
                    best_move = move
                if time.time()- start_time > time_limit :
                    break    
        self.last_choice_value=best_value
        self.last_choice_eval = best_eval
        self.last_choice_nodes=self.nodes_expanded
        self.last_choice_time=time.time() - start_time        
        return best_move



chance = Chance()
ROLL_PROBS = chance.possible_rolls() 


def effective_pos(pos: int) -> float:
    if pos == 25:
        return 25.5
    if pos == 26:
        return 14.0
    if pos == 27:
        return ROLL_PROBS[3] * 35 + (1 - ROLL_PROBS[3]) * 14
    if pos == 28:
        return ROLL_PROBS[2] * 35 + (1 - ROLL_PROBS[2]) * 14
    if pos == 29:
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
            if target > 29:
                continue
            if target in opp_poss:
                ai_threat_opp += ROLL_PROBS[roll]

    for o in opp_poss:
        for roll in range(1, 6):
            target = o + roll
            if target > 29:
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
    
