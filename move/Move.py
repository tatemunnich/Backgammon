from anytree import Node

from move.IllegalMoveException import IllegalMoveException
from board.Board import getOtherColor, getRelativePointLocation, Board
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
    str_move_list = [str(move).replace(color + " ", "") for move in move_list]
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
        self.hit = False
        if (not (1 <= self.start <= 24)) or (not (1 <= self.end <= 24)):
            raise IllegalMoveException("Invalid location")

    def getDieUsed(self):
        return self.die

    def apply(self, board: Board):
        if board.numAt(getOtherColor(self.color), self.end) > 1:
            raise IllegalMoveException("Other player occupies point " + str(self.end))

        # VALID MOVEMENT, check if hit
        if board.numAt(getOtherColor(self.color), self.end) == 1:
            board.removeFromLocation(getOtherColor(self.color), self.end)
            board.moveToBar(getOtherColor(self.color))
            self.hit = True

        board.removeFromLocation(self.color, self.start)
        board.moveToLocation(self.color, self.end)

    def __str__(self):
        res = str(self.start) + "/" + str(self.end)
        if self.hit:
            res += "*"
        return res

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
        self.hit = False
        if not (1 <= self.end <= 24):
            raise IllegalMoveException("Invalid location")

    def getDieUsed(self):
        return self.die

    def apply(self, board: Board):
        if board.numAt(getOtherColor(self.color), self.end) > 1:
            raise IllegalMoveException("Other player occupies the location " + str(self.end))

        # VALID MOVEMENT, check if hit
        if board.numAt(getOtherColor(self.color), self.end) == 1:
            board.removeFromLocation(getOtherColor(self.color), self.end)
            board.moveToBar(getOtherColor(self.color))
            self.hit = True

        board.moveFromBar(self.color)
        board.moveToLocation(self.color, self.end)

    def __str__(self):
        res = "bar/" + str(self.end)
        if self.hit:
            res += "*"
        return res

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return type(self) == type(other) and self.end == other.end and self.color == other.color


class TakeOffMovement:

    def __init__(self, color: str, die: int, start: int):
        self.color = color
        self.die = die
        self.start = start
        self.end = None
        if not (1 <= self.start <= 24):
            raise IllegalMoveException("Invalid location")

    def getDieUsed(self):
        return self.die

    def apply(self, board: Board):
        if getRelativePointLocation(self.color, self.start) > self.die:
            raise IllegalMoveException("Move cannot be made given the die value " + str(self.die))
        elif getRelativePointLocation(self.color, self.start) < self.die:
            if board.farthestBack(self.color) != self.start:
                raise IllegalMoveException(
                    "You must move the farthest back piece off that you can with die " + str(self.die))

        # VALID MOVEMENT
        board.removeFromLocation(self.color, self.start)
        board.moveOff(self.color)

    def __str__(self):
        return str(self.start) + "/off"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return type(self) == type(other) and self.start == other.start and self.color == other.color


class MoveNode(Node):

    def __init__(self, move, board_after: Board, deep: int, color=None, dice=None, die=None, **kwargs):
        super().__init__(move, **kwargs)
        # self.name holds move from Node class
        self.board_after = board_after
        self.color = color
        self.dice = dice
        self.die = die
        self.deep = deep

    def setBoardAfter(self, board_after):
        self.board_after = board_after

    def getBoardAfter(self):
        return self.board_after

    def __str__(self):
        res = ""
        if self.is_root:
            # res += str(self.dice) + ":"
            if self.is_leaf:
                res += "(no play)"
        else:
            # TODO: add doubles and single piece move printing
            parent = self.parent
            res += str(parent) + " " + str(self.name)
        return res.strip()

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.board_after)

    def __eq__(self, other):
        return type(self) == type(other) and self.board_after == other.board_after
