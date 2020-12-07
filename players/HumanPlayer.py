import re
from itertools import permutations

from board.Board import getPieceSymbol
from move.MovementFactory import generate_moves


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
