import time
import cProfile

from board.Board import Board, BLACK, WHITE, NONE
from board.Dice import Dice
from move.Move import getMove
from move.MovementFactory3 import generate_moves
import random


class Backgammon:

    def __init__(self, color1=BLACK, color2=WHITE):
        self.colors = [color1, color2]
        self.board = Board()
        self.dice = Dice()

    def playAgainstRandom(self):
        while self.board.getWinner() == NONE:
            self.dice.rollNoDoubles()
            moves = generate_moves(self.board, self.colors[0], self.dice, verbose=True)
            print("Black rolled: " + str(self.dice))
            move = random.choice(list(moves))
            self.board.applyBoard(move.getBoardAfter())
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
            self.board.applyBoard(move.getBoardAfter())
            print(self.board)
            time.sleep(2)

            if self.board.getWinner() != NONE:
                break
        print("Winner, " + self.board.getWinner() + "!")

    def runRandom(self, verbose=False):
        winner = NONE
        while winner == NONE:
            winner = self.runOnce(verbose=verbose)

        print("Winner, " + winner + "!")

    def runOnceBlack(self, verbose=False, roll=None):
        if verbose:
            print("")

        if roll is None:
            self.dice.rollNoDoubles()
        else:
            self.dice.setRoll(roll)
        if verbose:
            print("Black rolled: " + str(self.dice))
        moves = generate_moves(self.board, self.colors[0], self.dice)
        if verbose:
            print(str(len(moves)) + " moves: " + str(moves))
        move = random.choice(list(moves))
        self.board.applyBoard(move.getBoardAfter())
        if verbose:
            print(self.board)
            print("Black moved: " + str(move))

        return self.board.getWinner()

    def runOnceWhite(self, verbose=False, roll=None):
        if verbose:
            print("")

        if roll is None:
            self.dice.rollNoDoubles()
        else:
            self.dice.setRoll(roll)

        if verbose:
            print("White rolled: " + str(self.dice))
        moves = generate_moves(self.board, self.colors[1], self.dice)
        if verbose:
            print(str(len(moves)) + " moves: " + str(moves))
        move = random.choice(list(moves))
        self.board.applyBoard(move.getBoardAfter())
        if verbose:
            print(self.board)
            print("White moved: " + str(move))

        return self.board.getWinner()

    def runOnce(self, verbose=False, black_roll=None, white_roll=None):
        winner = self.runOnceBlack(verbose=verbose, roll=black_roll)
        if winner != NONE:
            return winner
        winner = self.runOnceWhite(verbose=verbose, roll=white_roll)
        return winner

    def test(self):
        self.board.testSetup1()
        print(self.board)
        self.runOnce(verbose=True, black_roll=(1, 2))


def runRandomTime():
    for i in range(20):
        b = Backgammon()
        b.runRandom(verbose=False)


cProfile.run('runRandomTime()')
