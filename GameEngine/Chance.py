import numpy as np 
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


    # def apply_roll(self, state, roll):
    #     """تطبيق نتيجة الرمية على الحالة → ترجع حالة جديدة"""
    #     # if state has player in house of horus and roll is not 1 then
    #     # move it to rebirth
    #     #
    #     pass
