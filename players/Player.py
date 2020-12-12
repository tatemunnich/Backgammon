from abc import ABC


class Player(ABC):
    def won(self, board, value):
        pass

    def lost(self, board, value):
        pass

    def get_move(self, backgammon):
        pass
