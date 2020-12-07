from board.Board import getOtherColor, BLACK


class Pips:
    MIN = 0
    MAX = 1

    @ staticmethod
    def apply(board, color):
        pips = board.pips(color)
        return (375 - pips) / 375


class EnemyPips:
    MIN = 0
    MAX = 1

    @staticmethod
    def apply(board, color):
        pips = board.pips(getOtherColor(color))
        return pips / 375


class PipRatio:
    MIN = None
    MAX = None

    @staticmethod
    def apply(board, color):
        # TODO: not bounded
        if board.getWinner() == color:
            return 1000000000
        return board.pips(getOtherColor(color)) / board.pips(color)


class FarthestBack:
    MIN = 0
    MAX = 1

    @staticmethod
    def apply(board, color):
        if board.numBar(color) > 0:
            left = 25
        else:
            home = 0 if color == BLACK else 25
            left = abs(home - board.farthestBack(color))
        return (25 - left) / 25


class NumOff:
    MIN = 0
    MAX = 1

    @staticmethod
    def apply(board, color):
        return board.numOff(color) / 15
