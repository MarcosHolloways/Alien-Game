import json
class Games_Stats():
    def __init__(self, confg):
        self.confg  = confg
        self.reset_stats()
        self.game_active = False
        with open("High_Score.json", 'r') as f_object:
            self.high_score = json.load(f_object)
    def reset_stats(self):
        self.ships_left = self.confg.ship_limit
        self.score = 0
        self.level = 1


