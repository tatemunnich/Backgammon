from move.IllegalMoveException import IllegalMoveException
from copy import deepcopy

BLACK = "BLACK"
WHITE = "WHITE"
NONE = "NONE"


def getScratch(board):
    return deepcopy(board)


def getOtherColor(color):
    if color == BLACK:
        return WHITE
    elif color == WHITE:
        return BLACK


def getDirection(color):
    if color == BLACK:
        return 1
    elif color == WHITE:
        return -1


def inHome(color, location):
    if color == BLACK:
        return 18 < location < 25
    elif color == WHITE:
        return 0 < location < 7


def getRelativePointLocation(color, point):
    if color == BLACK:
        return 25 - point
    elif color == WHITE:
        return point


class Board:

    def __init__(self):
        self.pointsContent = [0] * 26
        self.pointsContent[1] = 2
        self.pointsContent[12] = 5
        self.pointsContent[17] = 3
        self.pointsContent[19] = 5
        self.pointsContent[24] = -2
        self.pointsContent[13] = -5
        self.pointsContent[8] = -3
        self.pointsContent[6] = -5

        self.blackCheckers = {1, 12, 17, 19}
        self.whiteCheckers = {24, 13, 8, 6}

        self.blackCheckersTaken = 0
        self.whiteCheckersTaken = 0

        self.doubleCube = 1
        self.doublePossession = NONE

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
        self.pointsContent[1] = 2
        self.pointsContent[12] = 5
        self.pointsContent[17] = 3
        self.pointsContent[19] = 5
        self.pointsContent[24] = -2
        self.pointsContent[13] = -5
        self.pointsContent[8] = -3
        self.pointsContent[6] = -5

        self.blackCheckers = {1, 12, 17, 19}
        self.whiteCheckers = {24, 13, 8, 6}

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

            bar_num = self.numBar(WHITE)
            if i == 1 and bar_num > 6:
                strg += str(bar_num)
            elif bar_num >= 6 - i:
                strg += "O"
            else:
                strg += " "

            strg += " |"

            for j in range(19, 25):
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

        strg += "|                  |BAR|                  |\n"

        for i in range(5, 0, -1):
            strg += "|"

            for j in range(12, 6, -1):
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

            for j in range(6, 0, -1):
                strg += " "
                strg += self._printPiece(j, i)
                strg += " "

            strg += "| "

            off_num = self.numOff(WHITE)
            if off_num >= i:
                strg += "O"
            if off_num >= 5 + i:
                strg += "O"
            if off_num >= 10 + i:
                strg += "O"

            strg += "\n"

        strg += "+12-11-10--9--8--7-------6--5--4--3--2--1-+"
        return strg

    def __hash__(self):
        return hash(tuple(self.pointsContent))

    def __eq__(self, other):
        double_stuff = self.doubleCube == other.doubleCube and self.doublePossession == other.doublePossession
        return type(self) == type(other) and self.pointsContent == other.pointsContent and double_stuff

    def getCheckerSet(self, color):
        if color == BLACK:
            return self.blackCheckers
        elif color == WHITE:
            return self.whiteCheckers

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
            return abs(self.pointsContent[25])
        elif color == WHITE:
            return abs(self.pointsContent[0])

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
            self.pointsContent[25] += 1
        elif color == WHITE:
            self.pointsContent[0] -= 1

    def farthestBack(self, color):
        if color == BLACK:
            return min(self.blackCheckers)
        elif color == WHITE:
            return max(self.whiteCheckers)

    def allInHome(self, color):
        if self.numBar(color) != 0:
            return False
        return inHome(color, self.farthestBack(color))

    def getWinner(self):
        if self.pointsContent[25] == 15:
            return BLACK
        elif self.pointsContent[0] == -15:
            return WHITE
        else:
            return NONE

    def testSetup(self):
        # roll 5,1
        self.pointsContent = [0] * 26
        self.pointsContent[1] = 2
        self.pointsContent[12] = 5
        self.pointsContent[17] = 3
        self.pointsContent[19] = 5
        self.pointsContent[2] = -14
        self.pointsContent[7] = -1

        self.blackCheckers = {1, 12, 17, 19}
        self.whiteCheckers = {2, 7}

        self.blackCheckersTaken = 0
        self.whiteCheckersTaken = 0

    def testSetup2(self):
        # roll 1,2
        self.pointsContent = [0] * 26
        self.pointsContent[1] = 1
        self.pointsContent[5] = 1
        self.pointsContent[12] = 5
        self.pointsContent[17] = 3
        self.pointsContent[19] = 5
        self.pointsContent[2] = -14
        self.pointsContent[7] = -1

        self.blackCheckers = {1, 5, 12, 17, 19}
        self.whiteCheckers = {2, 7}

        self.blackCheckersTaken = 0
        self.whiteCheckersTaken = 0

    def testSetup3(self):
        # roll 1,2
        self.pointsContent = [0] * 26
        self.pointsContent[1] = 1
        self.pointsContent[12] = 6
        self.pointsContent[17] = 3
        self.pointsContent[19] = 5
        self.pointsContent[2] = -14
        self.pointsContent[7] = -1

        self.blackCheckers = {1, 12, 17, 19}
        self.whiteCheckers = {2, 7}

        self.blackCheckersTaken = 0
        self.whiteCheckersTaken = 0

    def testSetup4(self):
        # roll
        self.pointsContent = [0] * 26
        self.pointsContent[1] = 2
        self.pointsContent[12] = 5
        self.pointsContent[17] = 3
        self.pointsContent[19] = 5
        self.pointsContent[13] = -5
        self.pointsContent[8] = -3
        self.pointsContent[6] = -5

        self.blackCheckers = {1, 12, 17, 19}
        self.whiteCheckers = {24, 13, 8, 6}

        self.blackCheckersTaken = 0
        self.whiteCheckersTaken = 2

    def testSetup5(self):
        # roll 4,2 BLACK
        self.pointsContent = [0] * 26
        self.pointsContent[1] = 1
        self.pointsContent[2] = -2
        self.pointsContent[4] = -1
        self.pointsContent[5] = -1
        self.pointsContent[6] = -3
        self.pointsContent[8] = -1
        self.pointsContent[12] = 5
        self.pointsContent[13] = -5
        self.pointsContent[17] = 2
        self.pointsContent[19] = 4
        self.pointsContent[20] = 1
        self.pointsContent[22] = 1
        self.pointsContent[24] = -2

        self.blackCheckers = {1, 12, 17, 19, 20, 22}
        self.whiteCheckers = {24, 13, 8, 6, 5, 4, 2}

        self.blackCheckersTaken = 1
        self.whiteCheckersTaken = 0

    def testSetup6(self):
        # black roll 6,4
        self.pointsContent = [0] * 26
        self.pointsContent[1] = 2
        self.pointsContent[12] = 5
        self.pointsContent[17] = 3
        self.pointsContent[19] = 5
        self.pointsContent[24] = -2
        self.pointsContent[13] = -5
        self.pointsContent[4] = -3
        self.pointsContent[6] = -5

        self.blackCheckers = {12, 17, 19}
        self.whiteCheckers = {24, 13, 6, 4}

        self.blackCheckersTaken = 2
        self.whiteCheckersTaken = 0

    def testSetup7(self):
        # white roll 2,4
        self.pointsContent = [0] * 26
        self.pointsContent[7] = 2
        self.pointsContent[12] = 5
        self.pointsContent[17] = 3
        self.pointsContent[19] = 5

        self.pointsContent[4] = -1
        self.pointsContent[3] = -3
        self.pointsContent[1] = -10
        self.pointsContent[0] = -1

        self.blackCheckers = {7, 12, 17, 19}
        self.whiteCheckers = {4, 3, 1}

        self.blackCheckersTaken = 0
        self.whiteCheckersTaken = 0
