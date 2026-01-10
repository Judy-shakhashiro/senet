
from colorama import Fore, Back, Style
class Cell:
    def __init__(self,t,p):
        types=['Normal','Rebirth','Water','Happiness','Three_Truths','Re_Atoum','Horus']
        players=['Black','White',None]
        if t in types:
            self.type=t
        if p in players:
            self.player=p
class State:
    def __init__(self,):
        self.cells=self.initialize_board()
        self.white_pieces=0
        self.black_pieces=0
        self.current_player='White'  # or black
        self.winner=None
        self.game_over=False
        self.rolled_value=None
    

            
    def display(self):
        print("Displaying the board")
        print(Fore.RED + 'This text is red')
        for i in range(30):
           cell=self.cells[i]
           if cell.player=='White':
               print(Fore.WHITE + cell.type, end='')
           elif cell.player=='Black':
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
             list.append(Cell('Normal', 'White'))
            else:
             list.append(Cell('Normal','Black'))
        list.append(Cell('Rebirth',None))
        for i in range(10):
           list.append(Cell('Normal',None))
        list.append(Cell('Happiness',None))
        list.append(Cell('Water',None))
        list.append(Cell('Three_Truths',None))
        list.append(Cell('Re_Atoum',None))
        list.append(Cell('Horus',None))
        return list

 

    def move_piece(self,toss,cells,index):
       # here piece means the piece we want to move
       # check if there is a player in house of horus and it is different 
       # from the cell we want to move ,then we move it to rebirth
       if(cells[29].player is not None and index!=29):
            self.to_rebirth()
       
       # if newpiece location is water ,go to rebirth
       if cells[index+toss].type == 'Water':
            self.to_rebirth()
       # else if toss is 3 and cells[index].type is house of three truths then promote()
       if toss == 3 and cells[index].type == 'Three_Truths':
            self.promote(cells,index,self.current_player)
       # else if toss is 2 and cells[index].type is house of re-atoum then promote()
       elif toss == 2 and cells[index].type == 'Re_Atoum':
            self.promote(cells,index,self.current_player)
       # else if it is any toss cells[index].type is house of horus then promote()
       elif toss == 1 and cells[index].type == 'Horus':
            self.promote(cells,index,self.current_player)
       # else (alter between black and white)  if cells[index].player=='White' cells[index].player='Black' else cells[index].player='White'
       # return new state
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

    def copy(self):
        """تعيد نسخة عميقة من الحالة"""
        pass

    def is_equal(self, other_state):
        """تتحقق من تساوي حالتين"""
        pass
    def legal_moves(self, state):
        """ترجع قائمة بالحركات القانونية الممكنة في الحالة الحالية"""
        pass

    def apply_move(self, state, move):
        """تطبيق حركة وتحديث الحالة → ترجع حالة جديدة"""
        pass

    def is_end(self, state) -> bool:
        """التحقق من نهاية اللعبة"""
        pass

