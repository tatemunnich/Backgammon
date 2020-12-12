import math

from board.Board import getPieceSymbol, getOtherColor, NONE
from board.Dice import Dice
from move.Move import MoveNode
from move.MovementFactory import generate_moves
from players.Player import Player


class MinimaxPlayer(Player):
    def __init__(self, color, heuristic, ply=2, name="Max"):
        self.name = name
        self.color = color
        if ply > 2:
            raise Exception("don't do more than 2")
        self.ply = ply
        self.heuristic = heuristic

    def get_move(self, backgammon):
        board = backgammon.board
        current = MoveNode("start", board_after=board, deep=0)
        return expectiminimax(current, self.ply, self.color, self.heuristic, dice=backgammon.dice)[1]

    def __str__(self):
        return self.name + " (" + getPieceSymbol(self.color) + ")"


#########################

class AlphaBetaPlayer(Player):
    def __init__(self, color, heuristic, ply=2, name="Alpha"):
        self.name = name
        self.color = color
        if ply > 2:
            raise Exception("don't do more than 2")
        self.ply = ply
        self.heuristic = heuristic

    def get_move(self, backgammon):
        board = backgammon.board
        current = MoveNode("start", board_after=board, deep=0)
        return alpha_beta(current, self.ply, self.color, self.heuristic, dice=backgammon.dice)[1]

    def __str__(self):
        return self.name + " (" + getPieceSymbol(self.color) + ")"


##########################################################################################
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
        return children
    else:
        return generate_moves(board, color, dice)


def expectiminimax(move: MoveNode, ply, color, heuristic, dice=None):
    if ply > 2:
        raise Exception("don't do more than 2")

    board = move.board_after
    if ply == 0 or board.getWinner() != NONE:
        return heuristic.apply(board, color), move

    if dice:  # assume that it is color's move
        alpha = -math.inf
        return_move = None
        children = get_board_children(board, color, dice=dice)
        for new_move in children:
            new_alpha = expectiminimax(new_move, ply - 1, color, heuristic)[0]
            if new_alpha > alpha:
                return_move = new_move
                alpha = new_alpha

    else:  # assume that is not color's move
        roll_dict = get_board_children(board, getOtherColor(color))
        alpha = 0
        return_move = None
        for roll in roll_dict:
            roll_alpha = math.inf
            for new_move in roll_dict[roll]:
                roll_alpha = min(roll_alpha, expectiminimax(new_move, ply - 1, color, heuristic)[0])
            alpha = alpha + roll_alpha * probability[roll]

    return alpha, return_move


def alpha_beta(move: MoveNode, ply, color, heuristic, alpha=-math.inf, beta=math.inf, dice=None):
    if ply > 2:
        raise Exception("don't do more than 2")

    board = move.board_after
    if ply == 0 or board.getWinner() != NONE:
        return heuristic.apply(board, color), move

    if dice:  # assume that it is color's move
        value = -math.inf
        return_move = None
        children = get_board_children(board, color, dice=dice)
        for new_move in children:
            new_value = alpha_beta(new_move, ply - 1, color, heuristic, alpha, beta)[0]
            if new_value > value:
                return_move = new_move
                value = new_value
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, return_move

    else:  # assume that is not color's move
        roll_dict = get_board_children(board, getOtherColor(color))
        value = 0
        used_prob = 0
        return_move = None
        done = {}
        for roll in roll_dict:
            roll_value = math.inf
            for new_move in roll_dict[roll]:
                board_after = new_move.board_after
                if board_after in done:
                    new_value = done[board_after]
                else:
                    new_value = alpha_beta(new_move, ply - 1, color, heuristic, alpha, beta)[0]
                    done[board_after] = new_value
                roll_value = min(roll_value, new_value)
            value = value + roll_value * probability[roll]
            used_prob += probability[roll]
            upper_bound_value = value + heuristic.MAX * (1 - used_prob)
            beta = min(beta, upper_bound_value)
            if beta <= alpha:
                break
        return value, return_move
