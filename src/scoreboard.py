from typing import Iterable

class Scoreboard:
    def __init__(self):
        self.score = {}

    def __inc_score(self, ident, score):
        try:
            self.score[ident] += score
        except:
            self.score[ident] = 0
            self.score[ident] += score

    def reset_tournament(self):
        self.score = {}
    
    def add_score(self, winner_ident, loser_ident):
        self.__inc_score(winner_ident, 1)
        self.__inc_score(loser_ident, 0)

    def add_draw(self, first_ident, second_ident):
        self.__inc_score(first_ident, 1)
        self.__inc_score(second_ident, 1)

    def to_encode(self):
        return self.score
