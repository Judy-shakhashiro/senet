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



def evaluate(state: State)  :
    
#check win (must the 7 blocks out)
    if state.is_end():
        winner = state.winner()
        if winner == 1:  
            return 10000.0
        elif winner == 0:  
            return -10000.0

    position_weight = 2.0
    out_weight = 15.0
    special_hous_weight = 3.0
    swap_weight = 4.0

    score = 0.0

  
    score += out_weight * state.white_pieces
    score -= out_weight * state.black_pieces

    #evaluate the progress of blocks 
    for i, cell in enumerate(state.cells):
        if cell.player == 1:  
            if i <= 29:
                progress_value = (i / 30.0)  **2
                score += position_weight * progress_value
                if i >= 20:
                    score += position_weight * 1.5
                elif i >= 10:
                    score += position_weight * 1.0

        elif cell.player == 0:  
            if i <= 29:
                progress_value = (i / 30.0)  
                score -= position_weight * progress_value
                if i >= 20:
                    score -= position_weight * 1.5
                elif i >= 15:
                    score -= position_weight * 1.0

    # evaluate special houses
    if state.cells[25].player == 1:
        score += special_hous_weight * 2.0
    elif state.cells[25].player == 0:
        score -= special_hous_weight * 2.0

    if state.cells[26].player == 1:
        score -= special_hous_weight * 1.5
    elif state.cells[26].player == 0:
        score += special_hous_weight * 1.5

    if state.cells[27].player == 1:
        score += special_hous_weight * 0.5
    elif state.cells[27].player == 0:
        score -= special_hous_weight * 0.5

    if state.cells[28].player == 1:
        score += special_hous_weight * 0.7
    elif state.cells[28].player == 0:
        score -= special_hous_weight * 0.7

    if state.cells[29].player == 1:
        score += special_hous_weight * 1.5
    elif state.cells[29].player == 0:
        score -= special_hous_weight * 1.5
    #evaluate swap(probablity)
    ai_threat_opp = count_swap_opport(state, 1)
    score += swap_weight * ai_threat_opp

    opp_threat_ai = count_swap_opport(state, 0)
    score -= swap_weight * opp_threat_ai

    
    

    #evaluate swap(actual)
    swap_bonus = 0.0
    if state.last_hit == 1:
        swap_bonus = 20.0
    elif state.last_hit == 0:
        swap_bonus = -20.0
    
    score += swap_bonus


    return float(score)


# number of available swap opportunities
def count_swap_opport(state: State, player: int) -> int:
    count_opport = 0
    opponent = 1 - player
    for i in range(30):
        if state.cells[i].player == player:
            for j in range(30):
                if state.cells[j].player == opponent:
                    diff = j-i
                    if 1 <= diff <= 5:
                        count_opport += 1
    return int(count_opport)