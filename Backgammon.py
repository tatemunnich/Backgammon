from board.Board import Board, BLACK, WHITE, NONE
from board.Dice import Dice
from move.IllegalMoveException import IllegalMoveException
from move.Move import createFromString
from move.MovementFactory2 import generate_moves


class Backgammon:

    def __init__(self, color1=BLACK, color2=WHITE):
        self.colors = [color1, color2]
        self.board = Board()
        self.dice = Dice()

    def run(self):
        while self.board.getWinner() == NONE:
            # self.dice.roll()
            # print(self.dice)
            # print(self.board)
            # generate_moves(self.board, self.colors[0], self.dice)
            # self.getMove(self.colors[0])
            # if self.board.getWinner() != NONE:
            #     break

            print("")
            self.dice.roll()
            # self.dice.setRoll(1, 2)
            print(self.dice)
            print(self.board)
            generate_moves(self.board, self.colors[1], self.dice)
            self.getMove(self.colors[1])
            if self.board.getWinner() != NONE:
                break
        return "Winner, " + self.board.getWinner() + "!"

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
        self.board.testSetup4()
        self.run()


b = Backgammon()
b.test()
