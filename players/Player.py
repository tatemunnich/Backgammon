import random
from board.Board import BLACK, NONE, getOtherColor
from board.Dice import Dice
from move.Move import MoveNode
from move.MovementFactory import generate_moves


probability = {
    (1, 1): 1 / 36, (2, 1): 2 / 36, (3, 1): 2 / 36, (4, 1): 2 / 36, (5, 1): 2 / 36, (6, 1): 2 / 36,
    (2, 2): 1 / 36, (2, 3): 2 / 36, (2, 4): 2 / 36, (2, 5): 2 / 36, (2, 6): 2 / 36,
    (3, 3): 1 / 36, (3, 4): 2 / 36, (3, 5): 2 / 36, (3, 6): 2 / 36,
    (4, 4): 1 / 36, (4, 5): 2 / 36, (4, 6): 2 / 36,
    (5, 5): 1 / 36, (5, 6): 2 / 36,
    (6, 6): 1 / 36
}


def get_board_children(board, color, dice=None):
    if not dice:
        children = {}
        for roll in probability:
            moves = generate_moves(board, color, Dice(roll[0], roll[1]))
            children[roll] = moves
    else:
        return generate_moves(board, color, dice)
    return children


def h(board, color):
    points = board.getCheckers(color)
    home = 25 if color == BLACK else 0
    pips = 0
    for point in points:
        num_at = board.pointsContent[point]
        if num_at == 1:
            pips += num_at * (home - point)  # maybe treat blots differently
        else:
            pips += num_at * (home - point)
    pips += 25 * board.numBar(color)
    return pips


def expectiminimax(move: MoveNode, ply, color, dice=None):
    if ply > 2:
        raise Exception("don't do more than 2")
    board = move.board_after

    if board.getWinner() != NONE or ply == 0:
        return h(board, color), move

    if dice:  # assume that it is color's move
        alpha = 375
        return_move = None
        children = get_board_children(board, color, dice=dice)
        for new_move in children:
            new_alpha = expectiminimax(new_move, ply - 1, color)[0]
            if new_alpha < alpha:
                return_move = new_move
                alpha = new_alpha

    else:  # assume that is not color's move
        roll_dict = get_board_children(board, getOtherColor(color))
        alpha = 0
        return_move = None
        for roll in roll_dict:
            roll_alpha = 0
            for new_move in roll_dict[roll]:
                roll_alpha = max(roll_alpha, expectiminimax(new_move, ply - 1, color)[0])
            alpha = alpha + roll_alpha * probability[roll]

    return alpha, return_move


class MinimaxPlayer:
    def __init__(self, color, ply=2):
        self.color = color
        if ply > 2:
            raise Exception("don't do more than 2")
        self.ply = ply

    def get_move(self, backgammon):
        board = backgammon.board
        current = MoveNode("start", board_after=board, deep=0)
        return expectiminimax(current, self.ply, self.color, backgammon.dice)[1]

    def __str__(self):
        return self.color


class RandomPlayer:
    def __init__(self, color):
        self.color = color

    def get_move(self, backgammon):
        moves = generate_moves(backgammon.board, self.color, backgammon.dice)
        return random.choice(tuple(moves))

    def __str__(self):
        return self.color
