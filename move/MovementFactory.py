from copy import copy
from anytree import RenderTree, PreOrderIter

from board.Board import getOtherColor, getRelativePointLocation, getScratch, getDirection, Board
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


def getMovesForDoubles(color, distance_dict, starting_loc, root):
    # BASE CASES
    if not distance_dict:
        return

    if not starting_loc:
        return

    board = root.board_after
    #############################################

    # Pieces on bar
    if board.numBar(color) > 0:
        die_1 = max(distance_dict)
        die_2 = min(distance_dict)
        try:
            scratch = board.__deepcopy__()
            move = BarMovement(color, die_1, getRelativePointLocation(getOtherColor(color), die_1))
            move.apply(scratch)
            # apply die 1
            move_node = MoveNode(str(move), scratch, die=die_1, deep=root.deep+1, parent=root)
            distance_dict_1 = update_distance_dict(die_1, distance_dict)
            getMovesForDoubles(color, distance_dict_1, starting_loc, move_node)
        except IllegalMoveException:
            pass

        if die_1 != die_2:
            try:
                # apply die 2 if different
                scratch = board.__deepcopy__()
                move = BarMovement(color, die_2, getRelativePointLocation(getOtherColor(color), die_2))
                move.apply(scratch)
                # apply die 2
                move_node = MoveNode(str(move), scratch, die=die_2, deep=root.deep+1, parent=root)
                distance_dict_1 = update_distance_dict(die_2, distance_dict)
                getMovesForDoubles(color, distance_dict_1, starting_loc, move_node)
            except IllegalMoveException:
                pass

    # # Able to bear off
    elif board.allInHome(color):
        die_1 = max(distance_dict)
        die_2 = min(distance_dict)

        if die_1 >= getRelativePointLocation(color, board.farthestBack(color)):
            scratch = board.__deepcopy__()
            try:
                move = TakeOffMovement(color, die_1, board.farthestBack(color))
                move.apply(scratch)
                move_node = MoveNode(str(move), scratch, die=die_1, deep=root.deep+1, parent=root)
                distance_dict = update_distance_dict(die_1, distance_dict)
                new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                getMovesForDoubles(color, distance_dict, new_start, move_node)
            except IllegalMoveException:
                pass

        else:
            try:
                scratch = board.__deepcopy__()
                move = TakeOffMovement(color, die_1, starting_loc)
                move.apply(scratch)
                move_node = MoveNode(str(move), scratch, die=die_1, deep=root.deep+1, parent=root)
                distance_dict = update_distance_dict(die_1, distance_dict)
                new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                getMovesForDoubles(color, distance_dict, new_start, move_node)
            except IllegalMoveException:
                try:
                    scratch = board.__deepcopy__()
                    move = NormalMovement(color, die_1, starting_loc, starting_loc + die_1 * getDirection(color))
                    move.apply(scratch)
                    # apply die 1
                    move_node = MoveNode(str(move), scratch, die=die_1, deep=root.deep+1, parent=root)
                    distance_dict_1 = update_distance_dict(die_1, distance_dict)
                    new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                    getMovesForDoubles(color, distance_dict_1, new_start, move_node)
                except IllegalMoveException:
                    pass

                if die_1 != die_2:
                    try:
                        scratch = board.__deepcopy__()
                        move = NormalMovement(color, die_2, starting_loc, starting_loc + die_2 * getDirection(color))
                        move.apply(scratch)
                        # apply die 2
                        move_node = MoveNode(str(move), scratch, die=die_2, deep=root.deep+1, parent=root)
                        distance_dict_1 = update_distance_dict(die_2, distance_dict)
                        new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                        getMovesForDoubles(color, distance_dict_1, new_start, move_node)
                    except IllegalMoveException:
                        pass

            # don't apply either
            more_start = get_next_location_move_on(board.getCheckers(color), starting_loc, color)
            getMovesForDoubles(color, distance_dict, more_start, root)

    # All other cases: only normal moves remain
    else:
        die_1 = max(distance_dict)
        die_2 = min(distance_dict)
        try:
            scratch = board.__deepcopy__()
            move = NormalMovement(color, die_1, starting_loc, starting_loc + die_1 * getDirection(color))
            move.apply(scratch)
            # apply die 1
            move_node = MoveNode(str(move), scratch, die=die_1, deep=root.deep+1, parent=root)
            distance_dict_1 = update_distance_dict(die_1, distance_dict)
            new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
            getMovesForDoubles(color, distance_dict_1, new_start, move_node)
        except IllegalMoveException:
            pass

        if die_1 != die_2:
            try:
                # apply die 2 if different
                scratch = board.__deepcopy__()
                move = NormalMovement(color, die_2, starting_loc, starting_loc + die_2 * getDirection(color))
                move.apply(scratch)
                # apply die 2
                move_node = MoveNode(str(move), scratch, die=die_2, deep=root.deep+1, parent=root)
                distance_dict_1 = update_distance_dict(die_2, distance_dict)
                new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                getMovesForDoubles(color, distance_dict_1, new_start, move_node)

            except IllegalMoveException:
                pass

        # don't apply either
        more_start = get_next_location_move_on(board.getCheckers(color), starting_loc, color)
        getMovesForDoubles(color, distance_dict, more_start, root)
    return root


def generateMoves2(board: Board, color: str, dice: Dice, verbose=False):
    root = MoveNode("root", board_after=board, deep=0, color=color, dice=dice)
    getMovesForDoubles(color, dice.getDistances(), board.farthestBack(color), root)
    if verbose:
        print(board)
        print(dice)
        print(RenderTree(root).by_attr())
    height = root.height
    moves = set(PreOrderIter(root, filter_=lambda node: node.deep == height))  # TODO: change back to set
    if height == 1 and not dice.isDoubles():
        min_die = min(dice.getDice())
        max_die = max(dice.getDice())
        used_dict = {min_die: set(), max_die: set()}
        for move in moves:
            used_dict[move.die].add(move)
        if used_dict[min_die] and used_dict[max_die]:
            return used_dict[max_die]

    return moves
