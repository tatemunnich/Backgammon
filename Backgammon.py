import time
import cProfile

from board.Board import Board, BLACK, WHITE, NONE
from board.Dice import Dice
from move.Move import createFromString
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
            move = self.getMove(self.colors[1], moves)
            self.board.applyBoard(move.getBoardAfter())
            print(self.board)
            time.sleep(2)

            if self.board.getWinner() != NONE:
                break
        print("Winner, " + self.board.getWinner() + "!")

    def runRandom(self):
        verbose = False
        while self.board.getWinner() == NONE:
            if verbose:
                print("")
            self.dice.roll()
            if verbose:
                print("Black rolled: " + str(self.dice))
            moves = generate_moves(self.board, self.colors[0], self.dice)
            move = random.choice(list(moves))
            self.board.applyBoard(move.getBoardAfter())
            if verbose:
                print(self.board)

            # self.getMove(self.colors[0])
            if self.board.getWinner() != NONE:
                break

            if verbose:
                print("")
            self.dice.roll()
            if verbose:
                print("White rolled: " + str(self.dice))
            moves = generate_moves(self.board, self.colors[1], self.dice)
            move = random.choice(list(moves))
            self.board.applyBoard(move.getBoardAfter())
            if verbose:
                print(self.board)

            if self.board.getWinner() != NONE:
                break
        print("Winner, " + self.board.getWinner() + "!")

    def runOnceBlack(self):
        print("")
        self.dice.rollNoDoubles()
        # self.dice.setRoll(4, 6)
        print("Black rolled: " + str(self.dice))
        moves = generate_moves(self.board, self.colors[0], self.dice)
        move = random.choice(list(moves))
        self.board.applyBoard(move.getBoardAfter())
        print(self.board)
        print("Black moved: " + str(move))


        # self.getMove(self.colors[0])
        if self.board.getWinner() != NONE:
            print("Winner, " + self.board.getWinner() + "!")
            return

    def runOnceWhite(self):
        print("")
        self.dice.rollNoDoubles()
        # self.dice.setRoll(2, 4)
        print("White rolled: " + str(self.dice))
        moves = generate_moves(self.board, self.colors[1], self.dice)
        move = random.choice(list(moves))
        self.board.applyBoard(move.getBoardAfter())
        print(self.board)
        print("White moved: " + str(move))

        if self.board.getWinner() != NONE:
            print("Winner, " + self.board.getWinner() + "!")
            return

    def getMove(self, color, move_list):
        while True:
            text = input("Enter the move for " + color + ": ")
            move = createFromString(text, color, self.board, self.dice)
            if move in move_list:
                return move

    def test(self):
        self.board.testSetup7()
        self.runOnce()


def runRandom():
    for i in range(20):
        b = Backgammon()
        b.runRandom()


cProfile.run('runRandom()')