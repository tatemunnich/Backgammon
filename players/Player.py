import random
import re
from itertools import permutations

from board.Board import BLACK, NONE, getOtherColor, getPieceSymbol, WHITE, getDirection, Board
from board.Dice import Dice
from move.Move import MoveNode
from move.MovementFactory import generate_moves


class MinimaxPlayer:
    def __init__(self, color, ply=2, name="Max"):
        self.name = name
        self.color = color
        if ply > 2:
            raise Exception("don't do more than 2")
        self.ply = ply

    def get_move(self, backgammon):
        board = backgammon.board
        current = MoveNode("start", board_after=board, deep=0)
        return expectiminimax(current, self.ply, self.color, backgammon.dice)[1]

    def __str__(self):
        return self.name + " (" + getPieceSymbol(self.color) + ")"


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
    return (375 - pips) / 375


def expectiminimax(move: MoveNode, ply, color, dice=None):
    if ply > 2:
        raise Exception("don't do more than 2")

    board = move.board_after
    if board.getWinner() != NONE or ply == 0:
        return h(board, color), move

    if dice:  # assume that it is color's move
        alpha = 0
        return_move = None
        children = get_board_children(board, color, dice=dice)
        for new_move in children:
            new_alpha = expectiminimax(new_move, ply - 1, color)[0]
            if new_alpha > alpha:
                return_move = new_move
                alpha = new_alpha

    else:  # assume that is not color's move
        roll_dict = get_board_children(board, getOtherColor(color))
        alpha = 0
        return_move = None
        for roll in roll_dict:
            roll_alpha = 1
            for new_move in roll_dict[roll]:
                roll_alpha = min(roll_alpha, expectiminimax(new_move, ply - 1, color)[0])
            alpha = alpha + roll_alpha * probability[roll]

    return alpha, return_move

#########################################################################################################


class RandomPlayer:
    def __init__(self, color, name="Crazy Carl"):
        self.name = name
        self.color = color

    def get_move(self, backgammon):
        moves = generate_moves(backgammon.board, self.color, backgammon.dice)
        return random.choice(tuple(moves))

    def __str__(self):
        return self.name + " (" + getPieceSymbol(self.color) + ")"

##########################################################################################################


class HumanPlayer:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def get_move(self, backgammon):
        moves = generate_moves(backgammon.board, self.color, backgammon.dice)
        return get_move(self.color, moves)

    def __str__(self):
        return self.name + " (" + getPieceSymbol(self.color) + ")"


def get_move(color, move_list):
    move_list = list(move_list)
    while True:
        text = input("Enter the move for " + color + ": ")
        move_index = create_from_string(text, color, move_list)
        if move_index is not False:
            return move_list[move_index]


def create_from_string(text: str, color: str, move_list):
    input_list = text.split(" ")
    perms = permutations(input_list)
    regex = re.compile(color + r" \d-\d: ")
    str_move_list = [regex.sub("", str(move)) for move in move_list]
    if text in ["help", "-help", "-h", "list"]:
        print("These are the available moves: " + str(str_move_list))
        return False
    for move_list in perms:
        move = " ".join(move_list)
        if move in str_move_list:
            return str_move_list.index(move)

    return False


##########################################################################################################


class GnuPlayer:
    def __init__(self, color):
        self.name = "gnubg"
        if color != WHITE:
            raise Exception("Gnubg should be white to avoid confusion")
        self.color = color

    def get_move(self, backgammon):
        moves = generate_moves(backgammon.board, self.color, backgammon.dice)
        return random.choice(tuple(moves))

    def __str__(self):
        return self.name + " (" + getPieceSymbol(self.color) + ")"


def export_to_snowietxt(backgammon):
    current_player = backgammon.players[backgammon.on_roll]
    if type(current_player) != GnuPlayer:
        return False
    current_color = current_player.color
    direction = getDirection(current_color)
    other_player = backgammon.players[(backgammon.on_roll + 1) % 2]

    string = ""

    match_length = 0
    string += str(match_length) + ";"

    jacoby = 0
    string += str(jacoby) + ";0;1;"

    current_player = 0
    string += str(current_player) + ";"

    name = other_player.name
    string += "gnubg;" + str(name) + ";"

    crawford = 0
    string += str(crawford) + ";"

    score_0, score_1 = 0, 0
    string += str(score_0) + ";" + str(score_1) + ";"

    cube_value = backgammon.board.doubleCube
    string += str(cube_value) + ";"

    cube_possesion = -1  # don't give the computer the doubling cube
    string += str(cube_possesion) + ";"

    current_on_bar = backgammon.board.numBar(current_color)
    string += str(current_on_bar) + ";"

    points = reversed(backgammon.board.pointsContent[1:-1])
    points = [-direction*point for point in points]
    for point in points:
        string += str(point) + ";"

    other_on_bar = backgammon.board.numBar(getOtherColor(current_color))
    string += str(other_on_bar) + ";"

    die_1, die_2 = backgammon.dice.die1, backgammon.dice.die2
    string += str(die_1) + ";" + str(die_2) + ";"

    return string


def import_from_snowietxt(string: str):
    vals = string.split(";")
    if vals[4] != "1" or vals[6] != "gnubg":
        raise Exception("Invalid file")

    b = Board()
    b.doubleCube = int(vals[10])
    b.doublePossession = NONE if vals[11] == "0" else BLACK if vals[11] == "1" else WHITE
    b.blackCheckersTaken = int(vals[12])
    b.whiteCheckersTaken = int(vals[37])
    b.blackCheckers = set()
    b.whiteCheckers = set()
    black_count = 15 - b.blackCheckersTaken
    white_count = -15 + b.whiteCheckersTaken
    for point, v in enumerate(vals[13:37], 1):
        v = int(v)
        b.pointsContent[point] = v
        if v < 0:
            b.whiteCheckers.add(point)
            white_count -= v
        elif v > 0:
            b.blackCheckers.add(point)
            black_count -= v
    b.pointsContent[0] = black_count
    b.pointsContent[25] = white_count
    print(b.pointsContent)
    print(b)
    print(b.blackCheckers)
    print(b.whiteCheckers)
