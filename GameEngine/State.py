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