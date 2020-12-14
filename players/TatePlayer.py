from board.Board import getPieceSymbol
from players.MinimaxPlayer import MinimaxPlayer, AlphaBetaPlayer
from players.Player import Player
from players.heuristics import PipRatio, FarthestBack, NumOff


class TatePlayer(Player):
    def __init__(self, color, name="Tate Jr."):
        self.name = name
        self.color = color
        self.main = MinimaxPlayer(self.color, name=self.name, heuristic=PipRatio, ply=2)
        self.race = AlphaBetaPlayer(self.color, name=self.name, heuristic=FarthestBack, ply=1)
        self.off = AlphaBetaPlayer(self.color, name=self.name, heuristic=NumOff, ply=1)

    def get_move(self, backgammon):
        if not backgammon.board.is_race():
            return self.main.get_move(backgammon)
        elif not backgammon.board.allInHome(self.color):
            return self.race.get_move(backgammon)
        else:
            return self.off.get_move(backgammon)

    def __str__(self):
        return self.name + " (" + getPieceSymbol(self.color) + ")"
