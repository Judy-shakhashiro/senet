# 📁 PROJECT EXPORT FOR LLMs

## 📊 Project Information

- **Project Name**: `senet`
- **Generated On**: 2026-01-16 15:33:36 (Asia/Damascus / GMT+03:00)
- **Total Files Processed**: 19
- **Export Tool**: Easy Whole Project to Single Text File for LLMs v1.1.0
- **Tool Author**: Jota / José Guilherme Pandolfi

### ⚙️ Export Configuration

| Setting | Value |
|---------|-------|
| Language | `en` |
| Max File Size | `1 MB` |
| Include Hidden Files | `false` |
| Output Format | `both` |

## 🌳 Project Structure

```
├── 📁 __pycache__/
│   ├── 📄 GameController.cpython-313.pyc (1.8 KB)
│   └── 📄 GameController.cpython-314.pyc (1.67 KB)
├── 📁 AI/
│   ├── 📁 __pycache__/
│   │   ├── 📄 AIPlayer.cpython-313.pyc (9.82 KB)
│   │   └── 📄 AIPlayer.cpython-314.pyc (2.32 KB)
│   └── 📄 AIPlayer.py (7.28 KB)
├── 📁 GameEngine/
│   ├── 📁 __pycache__/
│   │   ├── 📄 Chance.cpython-313.pyc (1.54 KB)
│   │   ├── 📄 Chance.cpython-314.pyc (1.2 KB)
│   │   ├── 📄 Player.cpython-313.pyc (1.39 KB)
│   │   ├── 📄 Player.cpython-314.pyc (1.5 KB)
│   │   ├── 📄 State.cpython-313.pyc (15.12 KB)
│   │   └── 📄 State.cpython-314.pyc (11.72 KB)
│   ├── 📄 Chance.py (892 B)
│   ├── 📄 Player.py (482 B)
│   └── 📄 State.py (13.25 KB)
├── 📁 UI/
│   └── 📄 render.py
├── 📄 board.py (1.05 KB)
├── 📄 GameController.py (948 B)
├── 📄 main.py (1.02 KB)
└── 📄 state.py (1.86 KB)
```

## 📑 Table of Contents

**Project Files:**

- [📄 AI/AIPlayer.py](#📄-ai-aiplayer-py)
- [📄 GameEngine/Chance.py](#📄-gameengine-chance-py)
- [📄 GameEngine/Player.py](#📄-gameengine-player-py)
- [📄 GameEngine/State.py](#📄-gameengine-state-py)
- [📄 UI/render.py](#📄-ui-render-py)
- [📄 board.py](#📄-board-py)
- [📄 GameController.py](#📄-gamecontroller-py)
- [📄 main.py](#📄-main-py)
- [📄 state.py](#📄-state-py)

---

## 📈 Project Statistics

| Metric | Count |
|--------|-------|
| Total Files | 19 |
| Total Directories | 6 |
| Text Files | 9 |
| Binary Files | 10 |
| Total Size | 74.8 KB |

### 📄 File Types Distribution

| Extension | Count |
|-----------|-------|
| `.pyc` | 10 |
| `.py` | 9 |

## 💻 File Code Contents

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `__pycache__/GameController.cpython-313.pyc`
- `__pycache__/GameController.cpython-314.pyc`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `AI/__pycache__/AIPlayer.cpython-313.pyc`
- `AI/__pycache__/AIPlayer.cpython-314.pyc`

### <a id="📄-ai-aiplayer-py"></a>📄 `AI/AIPlayer.py`

**File Info:**
- **Size**: 7.28 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `AI/AIPlayer.py`
- **Relative Path**: `AI`
- **Created**: 2026-01-15 09:27:03 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-16 15:32:24 (Asia/Damascus / GMT+03:00)
- **MD5**: `9c30bb61e84febf17600140f65d56811`
- **SHA256**: `44c2a54d5d73ad97a060ba94d296bd745bbc9602c072a61003d43c9551cec1a2`
- **Encoding**: ASCII

**File code content:**

```python
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
    

```

---

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `GameEngine/__pycache__/Chance.cpython-313.pyc`
- `GameEngine/__pycache__/Chance.cpython-314.pyc`
- `GameEngine/__pycache__/Player.cpython-313.pyc`
- `GameEngine/__pycache__/Player.cpython-314.pyc`
- `GameEngine/__pycache__/State.cpython-313.pyc`
- `GameEngine/__pycache__/State.cpython-314.pyc`

### <a id="📄-gameengine-chance-py"></a>📄 `GameEngine/Chance.py`

**File Info:**
- **Size**: 892 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `GameEngine/Chance.py`
- **Relative Path**: `GameEngine`
- **Created**: 2026-01-15 09:27:03 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-16 08:10:18 (Asia/Damascus / GMT+03:00)
- **MD5**: `3324aae8586e05b4db12eed8bd423214`
- **SHA256**: `2ace7a96789ce6106c3a9ca30e002e6b3baf35a729083751d226a5f8fe4e50a2`
- **Encoding**: UTF-8

**File code content:**

```python
import numpy as np 
from typing import List, Tuple
class Chance:
    def possible_rolls(self):
        """ترجع قائمة بجميع القيم الممكنة لرمي العصي مع احتمالاتها"""
        return {1: 4/16, 2: 6/16, 3: 4/16, 4: 1/16, 5: 1/16}


    def roll_table(self):
        rolls = self.possible_rolls()
        options = list(rolls.keys())
        weights = list(rolls.values())
        result = np.random.choice(options, p=weights)
        return  result

    def outcomes(self):
        rolls = self.possible_rolls()
        return list(rolls.items())

    # def apply_roll(self, state, roll):
    #     """تطبيق نتيجة الرمية على الحالة → ترجع حالة جديدة"""
    #     # if state has player in house of horus and roll is not 1 then
    #     # move it to rebirth
    #     #
    #     pass

```

---

### <a id="📄-gameengine-player-py"></a>📄 `GameEngine/Player.py`

**File Info:**
- **Size**: 482 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `GameEngine/Player.py`
- **Relative Path**: `GameEngine`
- **Created**: 2026-01-15 09:27:03 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-15 16:25:04 (Asia/Damascus / GMT+03:00)
- **MD5**: `5d5f96df72c917bb2721aca163e983d6`
- **SHA256**: `9665601c1f3fde7ff26f677cad7691b868a304fac151b65dcd4afc9df8fca315`
- **Encoding**: UTF-8

**File code content:**

```python
from GameEngine.State import State
class Player:
    def policy(self, state: State):
        """تحدد الحركة التي سينفذها اللاعب بناءً على حالته"""
        pass

class HumanPlayer(Player):
    def policy(self, state):
        """إدخال من المستخدم"""
        pass

class RandomPlayer(Player):
    def policy(self, state):
        """اختيار عشوائي من الحركات القانونية"""
        pass

```

---

### <a id="📄-gameengine-state-py"></a>📄 `GameEngine/State.py`

**File Info:**
- **Size**: 13.25 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `GameEngine/State.py`
- **Relative Path**: `GameEngine`
- **Created**: 2026-01-15 09:27:03 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-16 15:24:57 (Asia/Damascus / GMT+03:00)
- **MD5**: `0fb31694b23511f1b664244116a52365`
- **SHA256**: `af94733c97f85d9ae0a2484bd9d842688c6b53f9c5e018e6e563e91109992497`
- **Encoding**: ASCII

**File code content:**

```python
from typing import Optional
from colorama import Fore, Back, Style
import copy
from GameEngine.Chance import Chance
class Cell:
    def __init__(self,t,p):
        types=['O','B','W','H','T','R','S']
        players=[0,1,None]
        if t in types:
            self.type=t
        if p in players:
            self.player=p
class State:
    def __init__(self,turnCount:int=0,last_hit = None):
        self.cells=self.initialize_board()
        self.white_pieces=0
        self.black_pieces=0
        self.current_player=1  
        self.winner_player=None
        self.game_over=False
        self.rolled_value=None
        self.turnCount = turnCount
        self.last_hit = last_hit
    
    def display(self):
        print(Fore.MAGENTA + "-------------------")
        for i in range(10):
            cell=self.cells[i]
            if cell.player==1:
                print(Fore.BLUE + cell.type, end=' ')
            elif cell.player==0:
                print(Fore.MAGENTA + cell.type, end=' ')
            else:
                print(Fore.RESET + cell.type, end=' ')
            if (i+1)%10==0:
                print() 
        for i in range(10,20):
            cell=self.cells[29-i]
            if cell.player==1:
                print(Fore.BLUE + cell.type, end=' ')
            elif cell.player==0:
                print(Fore.MAGENTA + cell.type, end=' ')
            else:
                print(Fore.RESET + cell.type, end=' ')
            if (i+1)%10==0:
                print()  
        for i in range(20,30):
            cell=self.cells[i]
            if cell.player==1:
                print(Fore.BLUE + cell.type, end=' ')
            elif cell.player==0:
                print(Fore.MAGENTA + cell.type, end=' ')
            else:
                print(Fore.RESET + cell.type, end=' ')
            
            if (i+1)%10==0:
                print()  
                    # New line after every 10 cells
        print(Fore.MAGENTA+"-------------------")
            

    def initialize_board(self):
        list=[]
        for i in range(14):
            if(i%2==0):
                list.append(Cell('O', 1))
            else:
                list.append(Cell('O',0))
        list.append(Cell('B',None))
        for i in range(10):
            list.append(Cell('O',None))
        list.append(Cell('H',None))
        list.append(Cell('W',None))
        list.append(Cell('T',None))
        list.append(Cell('R',None))
        list.append(Cell('S',None))
        return list



    def move_piece(self,index):
        self.last_hit=None
        # index is the index of the piece we want to move
        # here piece means the piece we want to move
        # check if there is a player in house of horus and it is different 
        # from the cell we want to move ,then we move it to rebirth
        #    if(cells[29].player is not None and index!=29):
        #         self.to_rebirth()
        
        # if newpiece location is water ,go to rebirth
        if index+self.rolled_value<30 and self.cells[index+self.rolled_value].type == 'W' :
            self.cells[index].player = None
            self.to_rebirth(index+self.rolled_value)
            self.turnCount+=1
            self.current_player ^=1
            return self
            
        # else if toss is 3 and cells[index].type is house of three truths then promote()
        if self.cells[27].player ==self.current_player:
            if self.rolled_value == 3 and index == 27:
                self.promote(index)
                
            else:
                self.cells[27].player = None
                self.to_rebirth(27)
            self.turnCount +=1
            self.current_player ^=1
            return self    
                
        # else if toss is 2 and cells[index].type is house of re-atoum then promote()
        if self.cells[28].player ==self.current_player:
            if self.rolled_value == 2 and index == 28:
                self.promote(index)
                
            else: 
                self.cells[28].player=None
                self.to_rebirth(28)
            self.turnCount +=1
            self.current_player ^=1  
            return self 
                

        # else if it is any toss cells[index].type is house of horus then promote()
        if self.cells[29].player ==self.current_player:
            if index==29:
                self.promote(index)
                self.turnCount += 1
                self.current_player ^= 1
                return self
                
        # if a pawn is in the happiness and we rolled is 5 and player wanna move it
        if self.cells[25].player ==self.current_player:
            if (self.rolled_value==5 and index==25):
                self.promote(index)
                self.turnCount += 1
                self.current_player ^= 1
                return self
        

        # else (alter between black and white or to an empty space) 
        if index+self.rolled_value<30:
                if(self.cells[index+self.rolled_value].player is not None and self.cells[index+self.rolled_value].player != self.current_player):
                    
                    self.cells[index+self.rolled_value].player=self.current_player
                    self.cells[index].player=self.current_player^1
                    self.last_hit=self.current_player
                    
                elif(self.cells[index+self.rolled_value].player is None):
                    self.cells[index+self.rolled_value].player=self.current_player
                    self.cells[index].player=None
                    
                    # print(f'moved to empty cell at index {index+self.rolled_value} of player{self.current_player}')
        # in order to return the state after move 
        # just write this state=state.move_piece(toss,state.cells,index)    
        self.turnCount +=1
        self.current_player ^= 1
        return self
    
    def legal_moves(self):
        # should include the promotions and rebirth
        # return a list of indices of pieces that can be moved
        #  based on rolled_value and current_player
        legal_moves_list=[]
        for i in range(26):
            cell=self.cells[i]
            if cell.player == self.current_player:
                if self.is_valid_move(i):
                    legal_moves_list.append(i)
        return legal_moves_list 

    def is_valid_move(self,index):
        # 1 should not skip house of happiness
        if(index < 25 and index+self.rolled_value>25):
            return False
        if (index==25 and self.rolled_value==5):
            return True
        # 2 should not go beyond the last cell
        if(index>29):
            return False
        # 3 it should be a pawn from the current player pawns
        cell=self.cells[index]
        if(cell.player != self.current_player):
            return False
        # 4 should not land on a cell occupied by the same color
        if(index+self.rolled_value<25 and self.cells[index+self.rolled_value].player == self.current_player):
            return False
        return True

    def promote(self,index):
        self.cells[index].player= None
        if (self.current_player==0):
            self.black_pieces+=1
        else:
            self.white_pieces+=1

    def to_rebirth(self,index):
        # move to rebirth and 
        # if there is a piece on the rebirth 
        # then move to the first empty cell before it
        self.cells[index].player=None
        if(self.cells[14].player is None):
            self.cells[14].player=self.current_player
            return
        else:
            for i in range(14,-1,-1):
                if(self.cells[i].player is None):
                    self.cells[i].player=self.current_player
                    # print(f'{index} rebirthed to {i}')
                    return
            
    def play(self):
        while True:
            self.display()
            #check win
            # self.current_player=self.current_player ^ 1
            if(self.white_pieces==7):
                print(Fore.BLUE+'blue won !')
                return
            elif(self.black_pieces==7):
                print(Fore.MAGENTA+'magenta won !')
                return 
            chance=Chance()
            self.rolled_value=chance.roll_table()

            if self.current_player == 1 :
                print(Fore.BLUE+f'valid moves are: {self.legal_moves()}')
                print(Fore.BLUE+f'player blue rolled a {self.rolled_value}')
            else:
                print(Fore.MAGENTA+f'valid moves are: {self.legal_moves()}')
                print(Fore.MAGENTA+f'player magenta rolled a {self.rolled_value}')
            index=self.input()

            # legal_moves=self.legal_moves()
            # if(len(legal_moves)==0):
            #    print('no legal moves available ,turn skipped')
            #    continue
            # elif(index in legal_moves):
            while not self.is_valid_move(index):
                print(Fore.RED+'invalid move ,try again')
        
                index=self.input()
            self.move_piece(index)

    def copy(self):
        #return deep copy of the state
        return copy.deepcopy(self)
    
    def input(self):
        while True:
            index=input(Fore.WHITE+'Enter the index of the piece you want to move: ')
            try: 
                index=int(index)
                break
            except:
                print(Fore.RED+'Invalid move ,try again')
        return index


    def is_end(self) -> bool:
        if self.winner() is not None :
            return True
        return False
    
    def winner(self)->int:
        if self.black_pieces == 7:
            self.winner_player = "black"
            return 0
        if self.white_pieces==7:
            self.winner_player = "white" 
            return 1
        return None  
    def play_ai_vs_human(self,ai_player,chance,debug:bool=False):
        while not self.is_end():
            self.display()
            self.rolled_value=chance.roll_table()
            moves = self.legal_moves()
            if self.current_player ==1:
                print(Fore.BLUE + f"AI (blue) rolled {self.rolled_value}") 
                print(Fore.BLUE + f"Valid moves:{moves}") 
            else:
                print(Fore.MAGENTA + f"Human (magenta) rolled {self.rolled_value}")
                print(Fore.MAGENTA + f"Valid moves : {moves}")
            if not moves:
                print(Fore.YELLOW + "No valid moves == turn skipped")   
                self.current_player ^=1 
                self.turnCount +=1
                continue
            if self.current_player == 1:
                move = ai_player.choose_move(self,self.rolled_value)
                print(Fore.BLUE + f"AI choose move:{move}")
                if debug:
                        v = ai_player.last_choice_value
                        n = ai_player.last_choice_nodes
                        t = ai_player.last_choice_time
                        ev = ai_player.last_choice_eval
                        print(Fore.CYAN + f"[DEBUG] val={v}    eval={ev:}  nodes={n}  time={t:}s")
                self.move_piece(move)
            else:
                move = int(input(Fore.WHITE + "Enter index to move :"))
                while move not in moves:
                    print(Fore.RED + f"Invalid move, choose from: {moves}")  
                    move = int(input(Fore.WHITE + "Enter index to move: "))  
                self.move_piece(move)    
        if self.winner_player == "white":
            print(Fore.BLUE + "BLUE (AI) WON")
        else:
            print(Fore.MAGENTA + "MAGENTA (HUMAN) WON")             
    # def play_ai_vs_human(self, ai_player):
    #     chance = Chance()
    #     while not self.is_end():
    #         self.display()
    #         self.rolled_value = chance.roll_table()
    #         moves = self.legal_moves()
    #         if self.current_player == 1:
    #             print(Fore.BLUE + f"AI (blue) rolled {self.rolled_value}")
    #             print(Fore.BLUE + f"Valid moves: {moves}")
    #         else:
    #             print(Fore.MAGENTA + f"Human (magenta) rolled {self.rolled_value}")
    #             print(Fore.MAGENTA + f"Valid moves: {moves}")
        
    #         if not moves:
    #             print(Fore.YELLOW + "No valid moves → turn skipped")
    #             self.current_player ^= 1
    #             self.turnCount += 1
    #             continue

    #         if self.current_player == 1:
    #             move = ai_player.choose_move(self, self.rolled_value)
    #             print(Fore.BLUE + f"AI chooses move: {move}")
    #             self.move_piece(move)

    
    #         else:
    #             move = int(input(Fore.WHITE + "Enter index to move: "))
    #             while move not in moves:
    #                 print(Fore.RED + "Invalid move, choose from:", moves)
    #                 move = int(input(Fore.WHITE + "Enter index to move: "))
    #             self.move_piece(move)

    #     winner = self.winner_player
    #     if winner == "white":
    #         print(Fore.BLUE + "BLUE (AI) WON ")
    #     else:
    #         print(Fore.MAGENTA + "MAGENTA (HUMAN) WON ")
```

---

### <a id="📄-ui-render-py"></a>📄 `UI/render.py`

**File Info:**
- **Size**: 0 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `UI/render.py`
- **Relative Path**: `UI`
- **Created**: 2026-01-15 09:27:03 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-15 09:27:03 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```python

```

---

### <a id="📄-board-py"></a>📄 `board.py`

**File Info:**
- **Size**: 1.05 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `board.py`
- **Relative Path**: `root`
- **Created**: 2026-01-15 09:27:03 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-15 09:27:03 (Asia/Damascus / GMT+03:00)
- **MD5**: `b40b2061898460c4db34b47605554a72`
- **SHA256**: `e94d3bae92fd68399f6eeee6aba122c5968168d3684646fc0ce87c590a1f4312`
- **Encoding**: ASCII

**File code content:**

```python
class board:
    def __init__(self):
        self.cells=self.initialize_board()
        self.white_pieces=0
        self.black_pieces=0
        
    def display(self):
        print("Displaying the board")
        # to implement

    def initialize_board():
        list=[]
        for i in range(14):
            if(i%0==0):
             list.append(cell('Empty', 'White'))
            else:
             list.append(cell('Empty','Black'))
        list.append(cell('Rebirth',None))
        for i in range(10):
           list.append(cell('Empty',None))
        list.append('Happiness',None)
        list.append('Water',None)
        list.append('Three_Truths',None)
        list.append('Re_Atoum',None)
        list.append('Horus',None)
        return list


class cell:
    def __init__(self,t,p):
        types=['Empty','Rebirth','Water','Happiness','Three_Truths','Re_Atoum','Horus']
        players=['Black','White',None]
        if t in types:
            self.type=t
        if p in players:
            self.player=p

    
    


```

---

### <a id="📄-gamecontroller-py"></a>📄 `GameController.py`

**File Info:**
- **Size**: 948 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `GameController.py`
- **Relative Path**: `root`
- **Created**: 2026-01-15 09:27:03 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-15 16:25:04 (Asia/Damascus / GMT+03:00)
- **MD5**: `c97c8e80c46cc73ea6a31e3160e18cfe`
- **SHA256**: `9a17f07fbacc45cd9170b1a26a840e4ba051d2593c1ec7d1094916ce9de67aab`
- **Encoding**: ASCII

**File code content:**

```python
"""
Game Controller
"""
class GameController:
    def __init__(self, state, chance, player_max, player_min, view=None):
        self.state = state

        self.chance = chance
        self.players = {
            "MAX": player_max,
            "MIN": player_min
        }
        # self.view = view

    def game_loop(self):
        while not self.rules.is_end(self.state):
            current_player = self.state.current_player

            # 1. Chance
            roll = self.chance.roll()
            self.state = self.chance.apply_roll(self.state, roll)
            # self.view.show_roll(roll)

            # 2. Decision
            legal_moves = self.rules.legal_moves(self.state)
            move = self.players[current_player].policy(self.state)

            # 3. Transition
            self.state = self.rules.apply_move(self.state, move)

            # 4. Render
            # self.view.render(self.state)

```

---

### <a id="📄-main-py"></a>📄 `main.py`

**File Info:**
- **Size**: 1.02 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `main.py`
- **Relative Path**: `root`
- **Created**: 2026-01-15 09:27:03 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-16 15:33:36 (Asia/Damascus / GMT+03:00)
- **MD5**: `13324ba5af08405646addbbd7f9d82a7`
- **SHA256**: `c2d6c14928e622cf4e7067fec65c889a6f2154c133e9ea56d66c138bb8dab00a`
- **Encoding**: ASCII

**File code content:**

```python
"""
This is main file where is an entry point to our project
"""
from GameEngine.State import State
from GameEngine.Chance import Chance
from GameEngine.Player import HumanPlayer
from AI.AIPlayer import AIPlayer
from GameController import GameController
from colorama import Fore, Back, Style
def main():
    state = State()
    chance = Chance()
    depth = int(input(Fore.WHITE + "Enter deptth you wanna to play with:"))
    debug = input("Show AI debug info? (y/n): ").strip().lower() == "y"
    ai_player = AIPlayer(chance_model=chance,max_depth = depth,debug=debug)
    state.play_ai_vs_human(ai_player,chance,debug=debug)
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

```

---

### <a id="📄-state-py"></a>📄 `state.py`

**File Info:**
- **Size**: 1.86 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `state.py`
- **Relative Path**: `root`
- **Created**: 2026-01-15 09:27:03 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-15 09:27:03 (Asia/Damascus / GMT+03:00)
- **MD5**: `e3decceb979a84e34612aae16e2442fd`
- **SHA256**: `5e8c369d7dfb53dc059a8b319fb84858f0036e3e462a596941ebf33d49f2ac89`
- **Encoding**: ASCII

**File code content:**

```python
from board import cell
class state:
    def __init__(self):
      pass

    def play_toss(self):
        # to implement based on the probabilities tabel
        pass
    
    def move_piece(self,toss,cells,index):
       #here piece means the piece we want to move
       # check if there is a player in house of houros and it is different 
       # from the cell we want to move ,then we move it to rebirth
       # if newpiece location is water ,o to rebirth
       # else if toss is 3 and cells[index].t is house of three truths then promote()
       # else if toss is 2 and cells[index].t is house of re-atoum then promote()
       # else if it is ant toss cells[index].t is house of horus then promote()
       # else (alter between black and white)  if cells[index].p=='White' cells[index].p='Black' else cells[index].p='White'

       pass
    def is_valid_move(self,toss,cell,index):
        # 1 should not skip house of happiness
        # 2 should not be a cell of the same color
       
        pass
    def promote(self,board,index,player):
        board.cells[index].p= None
        if (player=='Black'):
            board.black_pieces
        else:    
          board.white_pieces
    def to_rebirth(self):
       # if there is a piece on the house 
       pass
    def play(self,board):
     while True:
        #check win
        if(board.white_pieces==0):
         print('white won !')
         return
        elif(board.white_pieces==1):
            print('black won !')
            return 
        result=self.play_toss()
        # if there is a palyer in three truths and the result is not thre
        #  then 
        # move it to rebirth
        # if there is a player in re-Atoum and the result is not 2 
        #then 
        # move to rebirth


        # else 
        self.move_player()


        



        


```

---

