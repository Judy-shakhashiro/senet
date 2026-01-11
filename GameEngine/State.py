
from colorama import Fore, Back, Style
import copy
class Cell:
    def __init__(self,t,p):
        types=['Normal','Rebirth','Water','Happiness','Three_Truths','Re_Atoum','Horus']
        players=[0,1,None]
        if t in types:
            self.type=t
        if p in players:
            self.player=p
class State:
    def __init__(self,):
        self.cells=self.initialize_board()
        self.white_pieces=0
        self.black_pieces=0
        self.current_player=1  # or black
        self.winner=None
        self.game_over=False
        self.rolled_value=None
    

            
    def display(self):
        print("Displaying the board")
        print(Fore.RED + 'This text is red')
        for i in range(30):
           cell=self.cells[i]
           if cell.player==1:
               print(Fore.WHITE + cell.type, end='')
           elif cell.player==0:
               print(Fore.BLACK + cell.type, end='')
           else:
               print(Fore.RESET + cell.type, end='')
           if (i+1)%10==0:
               print(Style.RESET_ALL)
               print()  # New line after every 10 cells

    def initialize_board(self):
        list=[]
        for i in range(14):
            if(i%2==0):
             list.append(Cell('Normal', 1))
            else:
             list.append(Cell('Normal',0))
        list.append(Cell('Rebirth',None))
        for i in range(10):
           list.append(Cell('Normal',None))
        list.append(Cell('Happiness',None))
        list.append(Cell('Water',None))
        list.append(Cell('Three_Truths',None))
        list.append(Cell('Re_Atoum',None))
        list.append(Cell('Horus',None))
        return list

 

    def move_piece(self,index):
       # index is the index of the piece we want to move
       # here piece means the piece we want to move
       # check if there is a player in house of horus and it is different 
       # from the cell we want to move ,then we move it to rebirth
    #    if(cells[29].player is not None and index!=29):
    #         self.to_rebirth()
       
       # if newpiece location is water ,go to rebirth
       if self.cells[index+self.rolled_value].type == 'Water' and self.cells[index+self.rolled_value].player is not self.current_player:
            self.to_rebirth(index)
       # else if toss is 3 and cells[index].type is house of three truths then promote()
       if self.cells[27].player is not None:
            if self.rolled_value == 3 and index == 27:
             self.promote(index)
            else:
             self.to_rebirth(index)
       # else if toss is 2 and cells[index].type is house of re-atoum then promote()
       elif self.cells[28].player is not None:
           if self.rolled_value == 2 and index == 28:
            self.promote(index)
           else: 
                self.to_rebirth(index)

       # else if it is any toss cells[index].type is house of horus then promote()
       elif self.cells[29].player is not None:
        if index==29:
           self.promote(index)
        else:
            self.to_rebirth(index)

       # else (alter between black and white or to an empty space) 
       else:
                if(self.cells[index+self.rolled_value].player != self.current_player or self.cells[index+self.rolled_value].player is None):
                    self.cells[index+self.rolled_value].player=self.current_player
                    self.cells[index].player=None
        # in order to return the state after move 
        # just write this state=state.move_piece(toss,state.cells,index)
   
         
                
    def legal_moves(self):
        # return a list of indices of pieces that can be moved
        #  based on rolled_value and current_player
        legal_moves_list=[]
        for i in range(30):
           cell=self.cells[i]
           if cell.player == self.current_player:
              if self.is_valid_move(i):
                legal_moves_list.append(i)
        return legal_moves_list 

    def is_valid_move(self,index):
        # 1 should not skip house of happiness
        if(index < 25 and index+self.rolled_value>25):
            return False
        # 2 should not land on a cell occupied by the same color
        if(self.cells[index+self.rolled_value].player == self.current_player):
            return False
        # 3 should not go beyond the last cell
        if(index+self.rolled_value>29):
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
          for i in range(13,-1,-1):
             if(self.cells[i].player is None):
                self.cells[i].player=self.current_player
                return



    def play(self):
     while True:
        #check win
        if(self.white_pieces==7):
         print('white won !')
         return
        elif(self.black_pieces==7):
            print('black won !')
            return 
        result=self.play_toss()
        self.move_player()

    def copy(self):
     #return deep copy of the state
      return copy.deepcopy(self)
       
    def is_end(self) -> bool:
        if(self.black_pieces==7 or self.white_pieces==7):
           return True
        return False