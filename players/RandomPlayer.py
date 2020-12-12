import random

from board.Board import getPieceSymbol
from move.MovementFactory import generate_moves
from players.Player import Player


class RandomPlayer(Player):
    def __init__(self, color, name="Crazy Carl"):
        self.name = name
        self.color = color

    def get_move(self, backgammon):
        moves = generate_moves(backgammon.board, self.color, backgammon.dice)
        return random.choice(tuple(moves))

    def __str__(self):
        return self.name + " (" + getPieceSymbol(self.color) + ")"
