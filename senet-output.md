# 📁 PROJECT EXPORT FOR LLMs

## 📊 Project Information

- **Project Name**: `senet`
- **Generated On**: 2026-01-18 14:54:40 (Asia/Damascus / GMT+03:00)
- **Total Files Processed**: 17
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
│   │   ├── 📄 AIPlayer.cpython-313.pyc (10.1 KB)
│   │   └── 📄 AIPlayer.cpython-314.pyc (12.19 KB)
│   └── 📄 AIPlayer.py (8.46 KB)
├── 📁 GameEngine/
│   ├── 📁 __pycache__/
│   │   ├── 📄 Chance.cpython-313.pyc (1.46 KB)
│   │   ├── 📄 Chance.cpython-314.pyc (1.5 KB)
│   │   ├── 📄 Player.cpython-313.pyc (1.3 KB)
│   │   ├── 📄 Player.cpython-314.pyc (1.5 KB)
│   │   ├── 📄 State.cpython-313.pyc (15.4 KB)
│   │   └── 📄 State.cpython-314.pyc (16.6 KB)
│   ├── 📄 Chance.py (615 B)
│   ├── 📄 Player.py (482 B)
│   └── 📄 State.py (12.4 KB)
├── 📄 board.py (1.05 KB)
├── 📄 main.py (996 B)
└── 📄 state.py (1.86 KB)
```

## 📑 Table of Contents

**Project Files:**

- [📄 AI/AIPlayer.py](#📄-ai-aiplayer-py)
- [📄 GameEngine/Chance.py](#📄-gameengine-chance-py)
- [📄 GameEngine/Player.py](#📄-gameengine-player-py)
- [📄 GameEngine/State.py](#📄-gameengine-state-py)
- [📄 board.py](#📄-board-py)
- [📄 main.py](#📄-main-py)
- [📄 state.py](#📄-state-py)

---

## 📈 Project Statistics

| Metric | Count |
|--------|-------|
| Total Files | 17 |
| Total Directories | 5 |
| Text Files | 7 |
| Binary Files | 10 |
| Total Size | 89.31 KB |

### 📄 File Types Distribution

| Extension | Count |
|-----------|-------|
| `.pyc` | 10 |
| `.py` | 7 |

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
- **Size**: 8.46 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `AI/AIPlayer.py`
- **Relative Path**: `AI`
- **Created**: 2026-01-17 20:11:16 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-18 14:54:39 (Asia/Damascus / GMT+03:00)
- **MD5**: `9690b400228127afee75555c6bbbfded`
- **SHA256**: `440ab9da9d204fba32e7e1f26476a5c38e73c296d34f8b295c2e846adcfa3418`
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
    
    def max_node_after_throw(self, state: State, options: int, depth: int ,alpha:float,beta:float, return_tuple: bool = False):
        copy_state=state.copy()
        copy_state.rolled_value=options
        moves = copy_state.legal_moves()
        if not moves:
            child = self.pass_turn(copy_state)
            return self.expectiminimax(child, depth - 1 ,alpha,beta)
        # def move_sorted(move):
        #     temp_child = copy_state.copy()
        #     temp_child.move_piece(move)
        #     return evaluate(temp_child)
        # moves = sorted(moves,key=move_sorted,reverse=True)
        best_value = -math.inf
        best_move = None
        best_eval = None
        for move in moves:
            child = copy_state.copy()
            child.move_piece(move) 
            evaluate_state = evaluate(child)
            value = self.expectiminimax(child, depth - 1,alpha,beta)
            if value > best_value:
                best_value = value
                best_move = move
                best_eval = evaluate_state
            # alpha = max(alpha,best_value)
            # if alpha >=beta:
            #     break
        if return_tuple:
            return best_value, best_move, best_eval
        return best_value

    def min_node_after_throw(self, state: State, options: int, depth: int,alpha:float,beta:float, return_tuple: bool = False):
        copy_state=state.copy()
        copy_state.rolled_value=options
        moves = copy_state.legal_moves()
        if not moves:
            child = self.pass_turn(copy_state)
            return self.expectiminimax(child, depth - 1,alpha,beta)
        # def move_sorted(move):
        #     temp_child = copy_state.copy()
        #     temp_child.move_piece(move)
        #     return evaluate(temp_child)
        # moves = sorted(moves,key=move_sorted)
        best_value = math.inf
        best_move = None
        best_eval = None
        for move in moves:
            child = copy_state.copy()
            child.move_piece(move)
            evaluate_state = evaluate(child)
            value = self.expectiminimax(child, depth - 1,alpha,beta)
            if value < best_value:
                best_value = value
                best_move = move
                best_eval = evaluate_state
            # beta = min(beta,best_value)
            # if alpha>=beta:
            #     break
        if return_tuple:
            return best_value, best_move, best_eval
        return best_value

    def choose_move(self, state: State, options: int):
        self.reset_states()
        copy_state=state.copy()
        copy_state.rolled_value=options
        moves = copy_state.legal_moves()
        start_time = time.time()
        if not moves:
            self.last_choice_nodes=0
            self.last_choice_time=time.time() - start_time
            self.last_choice_value=None
            return None
        
        if state.current_player == 1:  
            best_value, best_move, best_eval = self.max_node_after_throw(copy_state, copy_state.rolled_value, self.max_depth, -math.inf, math.inf, return_tuple=True) 
            self.last_choice_value=best_value
            self.last_choice_eval = best_eval
            self.last_choice_nodes=self.nodes_expanded
            self.last_choice_time=time.time() - start_time  
            return best_move

        else:  
            best_value, best_move, best_eval = self.min_node_after_throw(copy_state, copy_state.rolled_value, self.max_depth, -math.inf, math.inf, return_tuple=True) 
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

    position_weight = 2.0 # وزن موقع الحجر
    out_weight = 15.0 # وزن نعطيه للحجر الذي خرج
    special_hous_weight = 3.0 #وزن نضربه بالحجر بالمواقع الخاصة
    swap_weight = 4.0 # وزن تبديل الحجرين

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
                progress_value = (i / 30.0)  **2
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
- **Size**: 615 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `GameEngine/Chance.py`
- **Relative Path**: `GameEngine`
- **Created**: 2026-01-17 20:11:16 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-17 20:11:16 (Asia/Damascus / GMT+03:00)
- **MD5**: `658cc917348fde6620a9d6c7937cf8a6`
- **SHA256**: `bfc37f350de002cbcc2e3b76ee820a6b61618625854d1ac17c5a9b9e8ab006ee`
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

   

```

---

### <a id="📄-gameengine-player-py"></a>📄 `GameEngine/Player.py`

**File Info:**
- **Size**: 482 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `GameEngine/Player.py`
- **Relative Path**: `GameEngine`
- **Created**: 2026-01-17 20:11:16 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-17 20:11:16 (Asia/Damascus / GMT+03:00)
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
- **Size**: 12.4 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `GameEngine/State.py`
- **Relative Path**: `GameEngine`
- **Created**: 2026-01-17 20:11:16 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-18 11:50:23 (Asia/Damascus / GMT+03:00)
- **MD5**: `60d630f44154746a22865f5161e4fc62`
- **SHA256**: `d6a2c0c9f713411cf39432f261220739b4b266f1b29e6ccac5a4f86e6a0810a1`
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
        #------------------
        ## special squares 
        #------------------
        
        # if newpiece location is water ,go to rebirth
        if index+self.rolled_value==26 :
            
            self.to_rebirth(index+self.rolled_value)
            # self.turnCount+=1
            # self.current_player ^=1
            return self
            
        # else if toss is 3 and cells[index].type is house of three truths then promote()
        if self.cells[27].player==self.current_player:
            if self.rolled_value == 3 and index == 27:
                self.promote(index)
                return self
            else:
                
                self.to_rebirth(27)
            # self.turnCount +=1
            # self.current_player ^=1
        
                
        # else if toss is 2 and cells[index].type is house of re-atoum then promote()
        if self.cells[28].player ==self.current_player:
            if self.rolled_value == 2 and index == 28:
                self.promote(index)
                return self 
            else: 
                self.to_rebirth(28)
            # self.turnCount +=1
            # self.current_player ^=1  
            
                

        # else if it is any toss cells[index].type is house of horus then promote()
        if self.cells[29].player==self.current_player:
            if index==29:
                self.promote(index)
                # self.turnCount += 1
                # self.current_player ^= 1
                return self
                
        # if a pawn is in the happiness and we rolled is 5 and player wanna move it
        if self.cells[25].player==self.current_player:
            if (self.rolled_value==5 and index==25):
                self.promote(index)
                # self.turnCount += 1
                # self.current_player ^= 1
                return self
        

        # else (alter between black and white or to an empty space) 
        if index+self.rolled_value<30:
                # we checked previously in the valid move if the taret is not the same color as the current pawn
               
                if(self.cells[index+self.rolled_value].player is not None ):
                    self.cells[index+self.rolled_value].player=self.current_player
                    self.cells[index].player=self.current_player^1
                    self.last_hit=self.current_player
                    
                elif(self.cells[index+self.rolled_value].player is None):
                    self.cells[index+self.rolled_value].player=self.current_player
                    self.cells[index].player=None
                    
    
        # self.turnCount +=1
        # self.current_player ^= 1
        return self
    
    def legal_moves(self):
        # should include the promotions and rebirth
        # return a list of indices of pieces that can be moved
        #  based on rolled_value and current_player
        legal_moves_list=[]
        for i in range(30):
                if self.is_valid_move(i):
                    legal_moves_list.append(i)
        return legal_moves_list 

    def is_valid_move(self,index):
        # 1 should not skip house of happiness
        if(index < 25 and index+self.rolled_value>25):
            return False
        # if (index==25 and self.rolled_value==5):
        #     return True
        # 2 should not go beyond the last cell
        if(index>29):
            return False
        # 3 it should be a pawn from the current player pawns
        cell=self.cells[index]
        if(cell.player != self.current_player):
            return False
        # 4 should not land on a cell occupied by the same color
        #(can ğo from happiness to another special square)
        if(index+self.rolled_value<30 and self.cells[index+self.rolled_value].player == self.current_player):
            return False
        
        # 5 if it is three truths or re-atoum and we didn't ġet suitable roll ,then we can't move it
        if(index==28 and self.rolled_value!=2):
            return False
        if(index==27 and self.rolled_value!=3):
            return  False
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

            legal_moves=self.legal_moves()
            if(len(legal_moves)==0):
               print('no legal moves available ,turn skipped')
               continue
            elif(index in legal_moves):
                while not self.is_valid_move(index):
                    print(Fore.RED+'invalid move ,try again')
            
                    index=self.input()
            self.move_piece(index)
            self.turnCount +=1
            self.current_player ^= 1
            

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
    # def play(player1,player2):
    #     match player1:
    #      case 'human'


    def play_ai_vs_human(self, ai_player,debug: Optional[bool] = False):
        chance = Chance()
        while not self.is_end():
                if self.current_player == 0:
                    self.human_turn(chance)
                else:
                    self.ai_turn(chance, ai_player, debug)
        winner = self.winner_player
        if winner == "white":
            print(Fore.BLUE + "BLUE (AI) WON ")
        else:
            print(Fore.MAGENTA + "MAGENTA (HUMAN) WON ")



    def human_turn(self,chance):
            self.display()
            self.rolled_value = chance.roll_table()
            moves = self.legal_moves()
            print(Fore.MAGENTA + f"Human (magenta) rolled {self.rolled_value}")
            print(Fore.MAGENTA + f"Valid moves: {moves}")
            if not moves:
                print(Fore.YELLOW + "No valid moves -> turn skipped")
                self.current_player ^= 1
                self.turnCount += 1
                return
            move = self.input()
            while move not in moves:
                    print(Fore.RED + "Invalid move, choose from:", moves)
                    move = int(input(Fore.WHITE + "Enter index to move: "))    
            self.move_piece(move)
            self.turnCount +=1
            self.current_player ^= 1
            


    def random_turn():
        pass
    def last_pawn_turn():
        pass
    def ai_turn(self,chance,ai_player,debug: Optional[bool] = False):
        self.display()
        self.rolled_value = chance.roll_table()
        moves = self.legal_moves()
        print(Fore.BLUE + f"AI (blue) rolled {self.rolled_value}")
        print(Fore.BLUE + f"Valid moves: {moves}")
        if not moves:
            print(Fore.YELLOW + "No valid moves -> turn skipped")
            self.current_player ^= 1
            self.turnCount += 1
            return
        move = ai_player.choose_move(self, self.rolled_value)
        print(Fore.BLUE + f"AI chooses move: {move}")
        if debug:
            v = ai_player.last_choice_value
            n = ai_player.last_choice_nodes
            t = ai_player.last_choice_time
            ev = ai_player.last_choice_eval
            print(Fore.CYAN + f"[DEBUG] val={v}    eval={ev:}  nodes={n}  time={t:}s")
        self.move_piece(move)
        self.turnCount +=1
        self.current_player ^= 1

    
        

```

---

### <a id="📄-board-py"></a>📄 `board.py`

**File Info:**
- **Size**: 1.05 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `board.py`
- **Relative Path**: `root`
- **Created**: 2026-01-17 20:11:16 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-17 20:11:16 (Asia/Damascus / GMT+03:00)
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

### <a id="📄-main-py"></a>📄 `main.py`

**File Info:**
- **Size**: 996 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `main.py`
- **Relative Path**: `root`
- **Created**: 2026-01-17 20:11:16 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-17 20:11:16 (Asia/Damascus / GMT+03:00)
- **MD5**: `1ee05c11c3a35c4affc4fafd4e397674`
- **SHA256**: `fed5c7a1ae7af70d7ad5bedb1ce3fc8c6c85ab81370cab54604d036ed139fa6b`
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

from colorama import Fore, Back, Style
def main():
    state = State()
    chance = Chance()
    depth = int(input(Fore.WHITE + "Enter deptth you wanna to play with:"))
    debug = input("Show AI debug info? (y/n): ").strip().lower() == "y"
    ai_player = AIPlayer(chance_model=chance,max_depth = depth,debug=debug)
    state.play_ai_vs_human(ai_player,debug=debug)
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
- **Created**: 2026-01-17 20:11:16 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-01-17 20:11:16 (Asia/Damascus / GMT+03:00)
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

