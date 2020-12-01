from move.IllegalMoveException import IllegalMoveException
from board.Board import getOtherColor, getRelativePointLocation, Board


class NormalMovement:

    def __init__(self, color: str, start: int, end: int):
        self.color = color
        self.start = start
        self.end = end
        self.hit = False
        if (not (1 <= self.start <= 24)) or (not (1 <= self.end <= 24)):
            raise IllegalMoveException("Invalid location")

    def apply(self, board: Board):
        if board.numAt(getOtherColor(self.color), self.end) > 1:
            raise IllegalMoveException("Other player occupies point " + str(self.end))

        scratch = board.__deepcopy__()

        # VALID MOVEMENT, check if hit
        if scratch.numAt(getOtherColor(self.color), self.end) == 1:
            scratch.removeFromLocation(getOtherColor(self.color), self.end)
            scratch.moveToBar(getOtherColor(self.color))
            self.hit = True

        scratch.removeFromLocation(self.color, self.start)
        scratch.moveToLocation(self.color, self.end)

        return scratch

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

    def __init__(self, color: str, end: int):
        self.color = color
        self.end = end
        self.hit = False
        if not (1 <= self.end <= 24):
            raise IllegalMoveException("Invalid location")

    def apply(self, board: Board):
        if board.numAt(getOtherColor(self.color), self.end) > 1:
            raise IllegalMoveException("Other player occupies the location " + str(self.end))

        scratch = board.__deepcopy__()

        # VALID MOVEMENT, check if hit
        if scratch.numAt(getOtherColor(self.color), self.end) == 1:
            scratch.removeFromLocation(getOtherColor(self.color), self.end)
            scratch.moveToBar(getOtherColor(self.color))
            self.hit = True

        scratch.moveFromBar(self.color)
        scratch.moveToLocation(self.color, self.end)

        return scratch

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

        scratch = board.__deepcopy__()

        # VALID MOVEMENT
        scratch.removeFromLocation(self.color, self.start)
        scratch.moveOff(self.color)

        return scratch

    def __str__(self):
        return str(self.start) + "/off"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return type(self) == type(other) and self.start == other.start and self.color == other.color


class MoveNode:

    def __init__(self, name: str, board_after: Board, deep: int, die=None):
        self.children = []
        self.name = name
        self.board_after = board_after
        self.deep = deep
        self.die = die

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.board_after)

    def __eq__(self, other):
        return type(self) == type(other) and self.board_after == other.board_after

