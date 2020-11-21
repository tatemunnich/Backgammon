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
            print("")
            self.dice.rollNoDoubles()
            self.dice.setRoll(4, 2)
            print("Black rolled: " + str(self.dice))
            moves = generate_moves(self.board, self.colors[0], self.dice)
            move = random.choice(list(moves))
            self.board.applyBoard(move.getBoardAfter())
            print(self.board)

            # self.getMove(self.colors[0])
            if self.board.getWinner() != NONE:
                break

            print("")
            self.dice.rollNoDoubles()
            print("White rolled: " + str(self.dice))
            moves = generate_moves(self.board, self.colors[1], self.dice)
            move = random.choice(list(moves))
            self.board.applyBoard(move.getBoardAfter())
            print(self.board)

            if self.board.getWinner() != NONE:
                break
        return "Winner, " + self.board.getWinner() + "!"

    def runRandom(self):
        while self.board.getWinner() == NONE:
            print("")
            self.dice.roll()
            print("Black rolled: " + str(self.dice))
            moves = generate_moves(self.board, self.colors[0], self.dice)
            move = random.choice(list(moves))
            self.board.applyBoard(move.getBoardAfter())
            print(self.board)

            # self.getMove(self.colors[0])
            if self.board.getWinner() != NONE:
                break

            print("")
            self.dice.roll()
            print("White rolled: " + str(self.dice))
            moves = generate_moves(self.board, self.colors[1], self.dice)
            move = random.choice(list(moves))
            self.board.applyBoard(move.getBoardAfter())
            print(self.board)

            if self.board.getWinner() != NONE:
                break
        return "Winner, " + self.board.getWinner() + "!"

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

    def getMove(self, color):
        success = False
        while not success:
            text = input("Enter the move for " + color + ": ")
            move = createFromString(text, color, self.board, self.dice)
            print(move)
            if move:
                self.board.applyBoard(move.getBoardAfter())
                success = True

    def test(self):
        self.board.testSetup7()
        self.runOnce()


b = Backgammon()
b.runRandom()
