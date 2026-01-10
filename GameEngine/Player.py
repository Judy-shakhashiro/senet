class Player:
    def policy(self, state: GameState):
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
