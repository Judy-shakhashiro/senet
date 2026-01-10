"""
Game Controller
"""
class GameController:
    def __init__(self, state, rules, chance, player_max, player_min, view=None):
        self.state = state
        self.rules = rules
        self.chance = chance
        self.players = {
            "MAX": player_max,
            "MIN": player_min
        }
        # self.view = view

    def game_loop(self):
        while not self.rules.is_end(self.state):
            current_player = self.state.current_player

            # 1. Chance
            roll = self.chance.roll()
            self.state = self.chance.apply_roll(self.state, roll)
            # self.view.show_roll(roll)

            # 2. Decision
            legal_moves = self.rules.legal_moves(self.state)
            move = self.players[current_player].policy(self.state)

            # 3. Transition
            self.state = self.rules.apply_move(self.state, move)

            # 4. Render
            # self.view.render(self.state)
