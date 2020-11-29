from copy import copy
from anytree import PreOrderIter

from board.Board import getOtherColor, getRelativePointLocation, getDirection, Board
from board.Dice import Dice
from move.IllegalMoveException import IllegalMoveException
from move.Move import BarMovement, TakeOffMovement, NormalMovement, MoveNode


def update_distance_dict(die, distance_dict: dict):
    if die not in distance_dict:
        raise Exception("BAD!")

    distance_dict = copy(distance_dict)

    distance_dict[die] = distance_dict[die] - 1
    if distance_dict[die] == 0:
        distance_dict.pop(die)

    return distance_dict


def get_next_location(point_list, starting_loc, color):
    if starting_loc < 1 or starting_loc > 24:
        return False

    direc = getDirection(color)
    if direc == 1:
        for point in point_list:
            if point >= starting_loc:
                return point
    elif direc == -1:
        for point in point_list:
            if point <= starting_loc:
                return point

    return False


def get_next_location_move_on(point_list, starting_loc, color):
    if starting_loc < 1 or starting_loc > 24:
        return False

    direc = getDirection(color)
    if direc == 1:
        for point in point_list:
            if point > starting_loc:
                return point
    elif direc == -1:
        for point in point_list:
            if point < starting_loc:
                return point

    return False


def do_normal_move(color, distance_dict, starting_loc, root, board, die_1, die_2):
    direction = getDirection(color)
    try:
        move = NormalMovement(color, starting_loc, starting_loc + die_1 * direction)
        scratch = move.apply(board)
        # apply die 1
        move_node = MoveNode(root.name + " " + str(move), scratch, die=die_1, deep=root.deep + 1)
        root.children.append(move_node)
        distance_dict_1 = update_distance_dict(die_1, distance_dict)
        new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
        get_moves(color, distance_dict_1, new_start, move_node)
    except IllegalMoveException:
        pass

    if die_1 != die_2:
        try:
            move = NormalMovement(color, starting_loc, starting_loc + die_2 * direction)
            scratch = move.apply(board)
            # apply die 2
            move_node = MoveNode(root.name + " " + str(move), scratch, die=die_2, deep=root.deep + 1)
            root.children.append(move_node)
            distance_dict_1 = update_distance_dict(die_2, distance_dict)
            new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
            get_moves(color, distance_dict_1, new_start, move_node)

        except IllegalMoveException:
            pass

    # don't apply either
    more_start = get_next_location_move_on(board.getCheckers(color), starting_loc, color)
    get_moves(color, distance_dict, more_start, root)


def get_moves(color, distance_dict, starting_loc, root):
    # TODO: add doubles and single piece move printing
    # BASE CASES
    if not distance_dict:
        return

    if not starting_loc:
        return

    board = root.board_after
    die_1 = max(distance_dict)
    die_2 = min(distance_dict)
    #############################################

    # Pieces on bar
    if board.numBar(color) > 0:
        try:
            move = BarMovement(color, getRelativePointLocation(getOtherColor(color), die_1))
            scratch = move.apply(board)
            # apply die 1
            move_node = MoveNode(root.name + " " + str(move), scratch, die=die_1, deep=root.deep+1)
            root.children.append(move_node)
            distance_dict_1 = update_distance_dict(die_1, distance_dict)
            get_moves(color, distance_dict_1, starting_loc, move_node)
        except IllegalMoveException:
            if die_1 != die_2:
                try:
                    # apply die 2 if different
                    move = BarMovement(color, getRelativePointLocation(getOtherColor(color), die_2))
                    scratch = move.apply(board)
                    # apply die 2
                    move_node = MoveNode(root.name + " " + str(move), scratch, die=die_2, deep=root.deep+1)
                    root.children.append(move_node)
                    distance_dict_1 = update_distance_dict(die_2, distance_dict)
                    get_moves(color, distance_dict_1, starting_loc, move_node)
                except IllegalMoveException:
                    pass

    # # Able to bear off
    elif board.allInHome(color):
        farthest_back = board.farthestBack(color)
        if die_1 >= getRelativePointLocation(color, farthest_back):
            try:
                move = TakeOffMovement(color, die_1, farthest_back)
                scratch = move.apply(board)
                move_node = MoveNode(root.name + " " + str(move), scratch, die=die_1, deep=root.deep+1)
                root.children.append(move_node)
                distance_dict = update_distance_dict(die_1, distance_dict)
                new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                get_moves(color, distance_dict, new_start, move_node)
            except IllegalMoveException:
                pass

        else:
            try:
                move = TakeOffMovement(color, die_1, starting_loc)
                scratch = move.apply(board)
                move_node = MoveNode(root.name + " " + str(move), scratch, die=die_1, deep=root.deep+1)
                root.children.append(move_node)
                distance_dict = update_distance_dict(die_1, distance_dict)
                new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                get_moves(color, distance_dict, new_start, move_node)
            except IllegalMoveException:
                do_normal_move(color, distance_dict, starting_loc, root, board, die_1, die_2)

    # All other cases: only normal moves remain
    else:
        do_normal_move(color, distance_dict, starting_loc, root, board, die_1, die_2)


def generate_moves(board: Board, color: str, dice: Dice, verbose=False):
    root = MoveNode(color + " " + str(dice), board_after=board, deep=0)
    get_moves(color, dice.getDistances(), board.farthestBack(color), root)

    min_die = min(dice.getDice())
    max_die = max(dice.getDice())
    depth = 0
    used_dict = {min_die: set(), max_die: set()}
    moves_dict = {}
    for move in PreOrderIter(root):
        deep = move.deep
        if deep > depth:
            depth = deep

        if deep not in moves_dict:
            moves_dict[deep] = {move}
        else:
            moves_dict[deep].add(move)

        if depth == 1:
            used_dict[move.die].add(move)

    if depth == 1 and used_dict[min_die] and used_dict[max_die]:
        moves = used_dict[max_die]
    else:
        moves = moves_dict[depth]

    if verbose:
        print(board)
        print(dice)
        print(moves)

    return moves
