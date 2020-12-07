from move.IllegalMoveException import IllegalMoveException
from copy import copy

BLACK = "BLACK"
WHITE = "WHITE"
NONE = "NONE"


def getPieceSymbol(color):
    if color == BLACK:
        return "X"
    elif color == WHITE:
        return "O"


def getOtherColor(color):
    if color == BLACK:
        return WHITE
    elif color == WHITE:
        return BLACK


def getDirection(color):
    if color == BLACK:
        return -1
    elif color == WHITE:
        return 1


def inHome(color, location):
    if color == BLACK:
        return 0 < location < 7
    elif color == WHITE:
        return 18 < location < 25


def getRelativePointLocation(color, point):
    if color == BLACK:
        return point
    elif color == WHITE:
        return 25 - point


class Board:

    def __init__(self, pointsContent=None, blackCheckers=None, whiteCheckers=None,
                 blackCheckersTaken=0, whiteCheckersTaken=0, doubleCube=1, doublePossession=NONE):
        if whiteCheckers is None:
            whiteCheckers = {1, 12, 17, 19}
        if blackCheckers is None:
            blackCheckers = {24, 13, 8, 6}
        if pointsContent is None:
            pointsContent = [0] * 26
            pointsContent[1] = -2
            pointsContent[12] = -5
            pointsContent[17] = -3
            pointsContent[19] = -5
            pointsContent[24] = 2
            pointsContent[13] = 5
            pointsContent[8] = 3
            pointsContent[6] = 5
        self.pointsContent = pointsContent

        self.blackCheckers = blackCheckers
        self.whiteCheckers = whiteCheckers

        self.blackCheckersTaken = blackCheckersTaken
        self.whiteCheckersTaken = whiteCheckersTaken

        self.doubleCube = doubleCube
        self.doublePossession = doublePossession

    def __deepcopy__(self, memo={}):
        _copy = type(self)(copy(self.pointsContent), copy(self.blackCheckers),
                           copy(self.whiteCheckers), self.blackCheckersTaken, self.whiteCheckersTaken,
                           self.doubleCube, self.doublePossession)
        return _copy

    def applyBoard(self, other_board):
        self.pointsContent = other_board.pointsContent
        self.whiteCheckers = other_board.whiteCheckers
        self.blackCheckers = other_board.blackCheckers
        self.blackCheckersTaken = other_board.blackCheckersTaken
        self.whiteCheckersTaken = other_board.whiteCheckersTaken
        self.doubleCube = other_board.doubleCube
        self.doublePossession = other_board.doublePossession

    def reset(self):
        self.pointsContent = [0] * 26
        self.pointsContent[1] = -2
        self.pointsContent[12] = -5
        self.pointsContent[17] = -3
        self.pointsContent[19] = -5
        self.pointsContent[24] = 2
        self.pointsContent[13] = 5
        self.pointsContent[8] = 3
        self.pointsContent[6] = 5

        self.blackCheckers = {24, 13, 8, 6}
        self.whiteCheckers = {1, 12, 17, 19}

        self.blackCheckersTaken = 0
        self.whiteCheckersTaken = 0

        self.doubleCube = 1
        self.doublePossession = NONE

    def _printPiece(self, location, count):
        color = self.colorAt(location)
        key = "X" if color == BLACK else "O"
        num = self.numAt(color, location)
        if 5 <= count < num:
            return str(num)
        elif num >= count:
            return key
        else:
            return " "

    def __str__(self):
        strg = "+13-14-15-16-17-18------19-20-21-22-23-24-+\n"
        for i in range(1, 6):
            strg += "|"

            for j in range(13, 19):
                strg += " "
                strg += self._printPiece(j, i)
                strg += " "

            strg += "| "

            bar_num = self.numBar(BLACK)
            if i == 1 and bar_num > 6:
                strg += str(bar_num)
            elif bar_num >= 6 - i:
                strg += "X"
            else:
                strg += " "

            strg += " |"

            for j in range(19, 25):
                strg += " "
                strg += self._printPiece(j, i)
                strg += " "

            strg += "| "

            off_num = self.numOff(WHITE)
            if off_num >= i:
                strg += "0"
            if off_num >= 5 + i:
                strg += "0"
            if off_num >= 10 + i:
                strg += "0"

            strg += "\n"

        strg += "|                  |BAR|                  |\n"

        for i in range(5, 0, -1):
            strg += "|"

            for j in range(12, 6, -1):
                strg += " "
                strg += self._printPiece(j, i)
                strg += " "

            strg += "| "

            bar_num = self.numBar(WHITE)
            if i == 1 and bar_num > 6:
                strg += str(bar_num)
            elif bar_num >= 6 - i:
                strg += "0"
            else:
                strg += " "

            strg += " |"

            for j in range(6, 0, -1):
                strg += " "
                strg += self._printPiece(j, i)
                strg += " "

            strg += "| "

            off_num = self.numOff(BLACK)
            if off_num >= i:
                strg += "X"
            if off_num >= 5 + i:
                strg += "X"
            if off_num >= 10 + i:
                strg += "X"

            strg += "\n"

        strg += "+12-11-10--9--8--7-------6--5--4--3--2--1-+"
        return strg

    def __hash__(self):
        return hash((tuple(self.pointsContent), self.doubleCube, self.doublePossession))

    def __eq__(self, other):
        double_stuff = self.doubleCube == other.doubleCube and self.doublePossession == other.doublePossession
        return type(self) == type(other) and self.pointsContent == other.pointsContent and double_stuff

    def getCheckers(self, color):
        if color == BLACK:
            return sorted(self.blackCheckers, reverse=True)
        elif color == WHITE:
            return sorted(self.whiteCheckers)

    def colorAt(self, location):
        if self.pointsContent[location] < 0:
            return WHITE
        elif self.pointsContent[location] == 0:
            return NONE
        elif self.pointsContent[location] > 0:
            return BLACK

    def numAt(self, color, location):
        val = self.pointsContent[location]
        if color == BLACK:
            if val < 0:
                return 0
            else:
                return abs(val)
        elif color == WHITE:
            if val > 0:
                return 0
            else:
                return abs(val)
        elif color == NONE:
            return 0

    def numOff(self, color):
        if color == BLACK:
            return abs(self.pointsContent[0])
        elif color == WHITE:
            return abs(self.pointsContent[25])

    def numBar(self, color):
        if color == BLACK:
            return self.blackCheckersTaken
        elif color == WHITE:
            return self.whiteCheckersTaken

    def moveToLocation(self, color, location):
        if self.colorAt(location) == getOtherColor(color):
            raise IllegalMoveException("Unexpected error - other color pieces at location " + str(
                location) + " of color " + getOtherColor(color))
        if color == BLACK:
            self.pointsContent[location] += 1
            if self.pointsContent[location] == 1:
                self.blackCheckers.add(location)
        elif color == WHITE:
            self.pointsContent[location] -= 1
            if self.pointsContent[location] == -1:
                self.whiteCheckers.add(location)

    def removeFromLocation(self, color, location):
        if self.colorAt(location) != color:
            raise IllegalMoveException(
                "Unexpected error - no pieces at location " + str(location) + " of color " + color)
        if color == BLACK:
            self.pointsContent[location] -= 1
            if self.pointsContent[location] == 0:
                self.blackCheckers.remove(location)
        elif color == WHITE:
            self.pointsContent[location] += 1
            if self.pointsContent[location] == 0:
                self.whiteCheckers.remove(location)

    def moveToBar(self, color):
        if color == BLACK:
            self.blackCheckersTaken += 1
        elif color == WHITE:
            self.whiteCheckersTaken += 1

    def moveFromBar(self, color):
        if color == BLACK:
            self.blackCheckersTaken -= 1
        elif color == WHITE:
            self.whiteCheckersTaken -= 1

    def moveOff(self, color):
        if color == BLACK:
            self.pointsContent[0] += 1
        elif color == WHITE:
            self.pointsContent[25] -= 1

    def farthestBack(self, color):
        if color == BLACK:
            if self.blackCheckers:
                return max(self.blackCheckers)
            else:
                return 25
        elif color == WHITE:
            if self.whiteCheckers:
                return min(self.whiteCheckers)
            else:
                return 0

    def allInHome(self, color):
        if self.numBar(color) != 0:
            return False
        return inHome(color, self.farthestBack(color))

    def getWinner(self, game_value=False):
        if self.pointsContent[0] == 15:
            if game_value:
                value = 1
                if not self.allInHome(WHITE):
                    value = 2
                    if self.numBar(WHITE) > 0 or inHome(BLACK, self.farthestBack(WHITE)):
                        value = 3
                return BLACK, value
            else:
                return BLACK
        elif self.pointsContent[25] == -15:
            if game_value:
                value = 1
                if not self.allInHome(BLACK):
                    value = 2
                    if self.numBar(BLACK) > 0 or inHome(WHITE, self.farthestBack(BLACK)):
                        value = 3
                return WHITE, value
            else:
                return WHITE
        else:
            if game_value:
                return NONE, 1
            else:
                return NONE

    def pips(self, color):
        points = self.getCheckers(color)
        home = 0 if color == BLACK else 25
        pips = 0
        for point in points:
            num_at = self.numAt(color, point)
            pips += num_at * abs(home - point)
        pips += 25 * self.numBar(color)
        return pips
