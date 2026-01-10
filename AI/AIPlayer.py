from GameEngine.Player import Player
from GameEngine.State import State

class AIPlayer(Player):
    def __init__(self, depth: int):
        self.depth = depth
    def generate_children_boards(self, state: State):
        """توليد جميع الحالات الممكنة من الحالة الحالية"""
        pass

    def policy(self, state: State):
        """تطبيق Expectiminimax لتحديد أفضل حركة بعد الرمية"""
        pass

    def expectiminimax(self, state: State, depth: int, player_type):
        """خوارزمية البحث مع Chance nodes و Max/Min nodes"""
        pass

    def evaluate(self, state: State) -> float:
        """دالة تقييم heuristic للحالة"""
        pass
