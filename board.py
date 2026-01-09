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

    
    

