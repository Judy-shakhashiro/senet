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


        



        

