import re
from subprocess import Popen, PIPE
from board.Board import BLACK, NONE, getOtherColor, getPieceSymbol, WHITE, getDirection, Board
from move.Move import MoveNode
from move.MovementFactory import generate_moves
from players.Player import Player


class GnuPlayer(Player):
    def __init__(self, color):
        self.name = "gnubg"
        if color != WHITE:
            raise Exception("Gnubg should be white to avoid confusion")
        self.color = color

    def get_move(self, backgammon):
        moves = generate_moves(backgammon.board, self.color, backgammon.dice)
        if len(moves) == 1:
            return moves.pop()
        export_to_snowietxt(backgammon,
                            r"C:\users\tatem\onedrive\documents\my stuff\senior\ai\course-project-tate\interfacing\to_gnu.txt")
        p = Popen([r"C:\Program Files (x86)\gnubg\gnubg-cli.exe", "-q", "-t", "-c",
                   r"C:\users\tatem\onedrive\documents\my stuff\senior\ai\course-project-tate\interfacing\command.txt"],
                  stdout=PIPE, stdin=PIPE)
        outs, errs = p.communicate(timeout=10)
        p.wait()
        f = re.search(r"gnubg moves (.*)" + re.escape("."), outs.decode('ascii'))
        if not f:
            name = "couldn't find text of move, output below"
            if "gnubg offers to resign" in outs.decode('ascii'):
                board = backgammon.board
        else:
            name = f.group(1) + " from gnubg's point of view"
            board = import_from_snowietxt(
                r"C:\users\tatem\onedrive\documents\my stuff\senior\ai\course-project-tate\interfacing\from_gnu.txt")
        move = MoveNode(name, board, deep=0)
        return move

    def __str__(self):
        return self.name + " (" + getPieceSymbol(self.color) + ")"


def export_to_snowietxt(backgammon, outfile):
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

    other_on_bar = backgammon.board.numBar(getOtherColor(current_color))
    string += str(other_on_bar) + ";"

    points = reversed(backgammon.board.pointsContent[1:-1])
    points = [-direction * point for point in points]
    for point in points:
        string += str(point) + ";"

    current_on_bar = backgammon.board.numBar(current_color)
    string += str(current_on_bar) + ";"

    die_1, die_2 = backgammon.dice.die1, backgammon.dice.die2
    string += str(die_1) + ";" + str(die_2) + ";"

    while True:
        try:
            with open(outfile, "w") as f:
                f.write(string)
                break
        except PermissionError:
            print("encountered a permission error. attempting to write again")
            continue


def import_from_snowietxt(infile):
    # TODO: encountering permission denied which prevents move reading
    while True:
        try:
            with open(infile) as f:
                string = f.readline()
                break
        except PermissionError:
            print("encountered a permission error. attempting to read again")
            continue

    vals = string.split(";")
    if vals[4] != "1" or vals[6] != "gnubg":
        raise Exception("Invalid file")

    b = Board()
    b.doubleCube = int(vals[10])
    b.doublePossession = NONE if vals[11] == "0" else BLACK if vals[11] == "1" else WHITE
    b.blackCheckersTaken = int(vals[37])
    b.whiteCheckersTaken = int(vals[12])
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
    return b
