import time
import cProfile

from board.Board import Board, BLACK, WHITE, NONE, getOtherColor
from board.Dice import Dice
from move.Move import getMove
from move.MovementFactory import generate_moves
import random

from players.Player import RandomPlayer, MinimaxPlayer


class Backgammon:

    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.board = Board()
        self.dice = Dice()
        self.color = BLACK  # starting player black

    def playAgainstRandom(self):
        while self.board.getWinner() == NONE:
            self.dice.rollNoDoubles()
            moves = generate_moves(self.board, self.colors[0], self.dice, verbose=True)
            print("Black rolled: " + str(self.dice))
            move = random.choice(tuple(moves))
            self.board.applyBoard(move.board_after)
            print(self.board)
            # self.getMove(self.colors[0])
            if self.board.getWinner() != NONE:
                break

            print("")
            self.dice.rollNoDoubles()
            print("Black moved " + str(move))
            print("White rolled: " + str(self.dice))
            moves = generate_moves(self.board, self.colors[1], self.dice)
            move = getMove(self.colors[1], moves)
            self.board.applyBoard(move.board_after)
            print(self.board)
            time.sleep(2)

            if self.board.getWinner() != NONE:
                break
        print("Winner, " + self.board.getWinner() + "!")

    def reset(self):
        self.board = Board()
        self.color = BLACK

    def do_move(self, move):
        self.board.applyBoard(move.board_after)
        self.dice.roll()
        self.color = getOtherColor(self.color)

    def run(self, verbose=False):
        while True:
            if verbose:
                print("")
                print(str(self.players[0]) + " rolled: " + str(self.dice))
            move = self.players[0].get_move(self)
            self.do_move(move)
            if verbose:
                print(self.board)
                print(move)
            if self.board.getWinner() != NONE:
                if verbose:
                    print("Winner, " + self.board.getWinner())
                return self.board.getWinner()
            ##################################################
            if verbose:
                print("")
                print(str(self.players[1]) + " rolled: " + str(self.dice))
            move = self.players[1].get_move(self)
            self.do_move(move)
            self.board.applyBoard(move.board_after)
            if verbose:
                print(self.board)
                print(move)
            if self.board.getWinner() != NONE:
                if verbose:
                    print("Winner, " + self.board.getWinner())
                return self.board.getWinner()


def runRandomTime():
    b = Backgammon(RandomPlayer(BLACK), RandomPlayer(WHITE))
    for i in range(20):
        print(b.run(verbose=False))
        b.reset()


cProfile.run('runRandomTime()')

# b = Backgammon(MinimaxPlayer(BLACK), RandomPlayer(WHITE))
# for i in range(20):
#     print(b.run(verbose=False))
#     b.reset()
