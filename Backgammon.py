import cProfile

from board.Board import Board, BLACK, WHITE, NONE
from board.Dice import Dice

from players.Player import RandomPlayer, MinimaxPlayer, HumanPlayer, GnuPlayer, export_to_snowietxt


class Backgammon:

    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.board = Board()
        self.dice = Dice()
        self.on_roll = 0  # starting player 1

    def reset(self):
        self.board = Board()
        self.on_roll = 0

    def do_move(self, move):
        self.board.applyBoard(move.board_after)
        self.dice.roll()
        self.on_roll = (self.on_roll + 1) % 2

    def run(self, verbose=False):
        if verbose:
            print(self.board)
            print(str(self.players[self.on_roll]) + " goes first.")
        while True:
            if verbose:
                print("")
                print(str(self.players[self.on_roll]) + " rolled " + str(self.dice))
            move = self.players[self.on_roll].get_move(self)
            self.do_move(move)
            if verbose:
                print(self.board)
                print(export_to_snowietxt(self))
                print(move)
            if self.board.getWinner() != NONE:
                if verbose:
                    print("Winner, " + self.board.getWinner())
                return self.board.getWinner()
            ##################################################
            if verbose:
                print("")
                print(str(self.players[self.on_roll]) + " rolled " + str(self.dice))
            move = self.players[self.on_roll].get_move(self)
            self.do_move(move)
            self.board.applyBoard(move.board_after)
            if verbose:
                print(self.board)
                print(export_to_snowietxt(self))
                print(move)
            if self.board.getWinner() != NONE:
                if verbose:
                    print("Winner, " + self.board.getWinner())
                return self.board.getWinner()


def runRandomTime():
    b = Backgammon(RandomPlayer(BLACK), RandomPlayer(WHITE))
    for i in range(30):
        print(b.run(verbose=False))
        b.reset()


if __name__ == "__main__":
    b = Backgammon(RandomPlayer(BLACK), GnuPlayer(WHITE))
    b.run(verbose=True)
    b.reset()
    # cProfile.run('runRandomTime()')
