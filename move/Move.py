from typing import List
from board.Dice import Dice
from move.IllegalMoveException import IllegalMoveException
from board.Board import getDirection, getOtherColor, getRelativePointLocation, Board
from itertools import permutations


def getMove(color, move_list):
    move_list = list(move_list)
    while True:
        text = input("Enter the move for " + color + ": ")
        move_index = createFromString(text, color, move_list)
        if move_index:
            return move_list[move_index]


def createFromString(text: str, color: str, move_list):
    input_list = text.split(" ")
    perms = permutations(input_list)
    str_move_list = [str(move).replace(color+" ", "") for move in move_list]
    for move_list in perms:
        move = " ".join(move_list)
        if move in str_move_list:
            return str_move_list.index(move)

    return False


class NormalMovement:

    def __init__(self, color: str, die: int, start: int, end: int):
        self.color = color
        self.die = die
        self.start = start
        self.end = end
        if (not (1 <= self.start <= 24)) or (not (1 <= self.end <= 24)):
            raise IllegalMoveException("Invalid location")

    def getDieUsed(self):
        return self.die

    def apply(self, board: Board):
        if abs(self.end - self.start) != self.die:
            raise IllegalMoveException("Move cannot be made given the die value " + str(self.die))

        if board.numBar(self.color) > 0:
            raise IllegalMoveException("You must move from the bar first")

        if board.numAt(self.color, self.start) == 0:
            raise IllegalMoveException("You don't have enough pieces at the start " + str(self.start))

        if (self.start > self.end and getDirection(self.color) > 0) or (
                self.start < self.end and getDirection(self.color) < 0):
            raise IllegalMoveException("You can't move backwards")

        if board.numAt(getOtherColor(self.color), self.end) > 1:
            raise IllegalMoveException("Other player occupies point " + str(self.end))

        # VALID MOVEMENT, check if hit
        if board.numAt(getOtherColor(self.color), self.end) == 1:
            board.removeFromLocation(getOtherColor(self.color), self.end)
            board.moveToBar(getOtherColor(self.color))

        board.removeFromLocation(self.color, self.start)
        board.moveToLocation(self.color, self.end)

    def __str__(self):
        return str(self.start) + "/" + str(self.end)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return type(self) == type(
            other) and self.start == other.start and self.end == other.end and self.color == other.color


class BarMovement:

    def __init__(self, color: str, die: int, end: int):
        self.color = color
        self.die = die
        self.end = end
        if not (1 <= self.end <= 24):
            raise IllegalMoveException("Invalid location")

    def getDieUsed(self):
        return self.die

    def apply(self, board: Board):
        if self.die != getRelativePointLocation(getOtherColor(self.color), self.end):
            raise IllegalMoveException("Move cannot be made given the die value " + str(self.die))

        if board.numBar(self.color) == 0:
            raise IllegalMoveException("Must have pieces on bar")

        if board.numAt(getOtherColor(self.color), self.end) > 1:
            raise IllegalMoveException("Other player occupies the location " + str(self.end))

        # VALID MOVEMENT, check if hit
        if board.numAt(getOtherColor(self.color), self.end) == 1:
            board.removeFromLocation(getOtherColor(self.color), self.end)
            board.moveToBar(getOtherColor(self.color))

        board.moveFromBar(self.color)
        board.moveToLocation(self.color, self.end)

    def __str__(self):
        return "bar/" + str(self.end)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return type(self) == type(other) and self.end == other.end and self.color == other.color


class TakeOffMovement:

    def __init__(self, color: str, die: int, start: int):
        self.color = color
        self.die = die
        self.start = start
        if not (1 <= self.start <= 24):
            raise IllegalMoveException("Invalid location")

    def getDieUsed(self):
        return self.die

    def apply(self, board: Board):
        if board.numAt(self.color, self.start) == 0:
            raise IllegalMoveException("You don't have enough pieces at the start " + str(self.start))

        if not board.allInHome(self.color):
            raise IllegalMoveException("You must have all your pieces in home before taking off")

        if getRelativePointLocation(self.color, self.start) > self.die:
            raise IllegalMoveException("Move cannot be made given the die value " + str(self.die))
        elif getRelativePointLocation(self.color, self.start) < self.die:
            if board.farthestBack(self.color) != self.start:
                raise IllegalMoveException("You must move the farthest back piece off that you can with die " + str(self.die))

        # VALID MOVEMENT
        board.removeFromLocation(self.color, self.start)
        board.moveOff(self.color)

    def __str__(self):
        return str(self.start) + "/off"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return type(self) == type(other) and self.start == other.start and self.color == other.color


class Move:

    def __init__(self, board_before: Board, color: str, dice: Dice, movements: List[NormalMovement], board_after: Board):
        self.color = color
        self.dice = dice
        self.movements = movements
        self.board_before = board_before
        self.board_after = board_after
        if dice.isDoubles():
            self.distances = [dice.getDie1()] * 4
        else:
            self.distances = [dice.getDie1(), dice.getDie2()]
            
    def setBoardAfter(self, board_after):
        self.board_after = board_after

    def getBoardAfter(self):
        return self.board_after

    def __str__(self):
        strg = self.color
        for movement in self.movements:
            strg += " " + str(movement)
        if len(self.movements) == 0:
            strg += " could not move"
        return strg

    def __repr__(self):
        return str(self)

    def __hash__(self):
        if self.board_after is None:
            raise NameError("No Board after")
        return hash(self.board_after)

    def __eq__(self, other):
        if type(self) == type(other):
            if self.board_after is not None and other.board_after is not None:
                board_stuff = self.board_after == other.board_after
            else:
                raise NameError("Board after has not been initalized by one of the two moves")
            return self.color == other.color and board_stuff
        else:
            return False
