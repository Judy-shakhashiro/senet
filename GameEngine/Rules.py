class Rules:
    def legal_moves(self, state):
        """ترجع قائمة بالحركات القانونية الممكنة في الحالة الحالية"""
        pass

    def apply_move(self, state, move):
        """تطبيق حركة وتحديث الحالة → ترجع حالة جديدة"""
        pass

    def is_end(self, state) -> bool:
        """التحقق من نهاية اللعبة"""
        pass
