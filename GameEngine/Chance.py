import numpy as np 
from typing import List, Tuple
class Chance:
    def possible_rolls(self):
       
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

   
