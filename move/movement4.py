from copy import copy
from anytree import Node, RenderTree, PreOrderIter

from board.Board import getOtherColor, getRelativePointLocation, getScratch, getDirection, Board
from board.Dice import Dice
from move.IllegalMoveException import IllegalMoveException
from move.Move import BarMovement, TakeOffMovement, NormalMovement
import cProfile


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


def getMovesForDoubles(board, color, distance_dict, starting_loc, root):
    # BASE CASES
    if not distance_dict:
        return

    if not starting_loc:
        return

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
            move_node = Node(move, parent=root)
            distance_dict_1 = update_distance_dict(die_1, distance_dict)
            getMovesForDoubles(scratch, color, distance_dict_1, starting_loc, move_node)
        except IllegalMoveException:
            pass

        if die_1 != die_2:
            try:
                # apply die 2 if different
                scratch = board.__deepcopy__()
                move = BarMovement(color, die_2, getRelativePointLocation(getOtherColor(color), die_2))
                move.apply(scratch)
                # apply die 2
                move_node = Node(move, parent=root)
                distance_dict_1 = update_distance_dict(die_1, distance_dict)
                getMovesForDoubles(scratch, color, distance_dict_1, starting_loc, move_node)
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
                move_node = Node(move, parent=root)
                distance_dict = update_distance_dict(die_1, distance_dict)
                new_start = get_next_location(scratch.getCheckers(color), scratch.farthestBack(color), color)
                getMovesForDoubles(scratch, color, distance_dict, new_start, move_node)
            except IllegalMoveException:
                pass

        else:
            try:
                scratch = board.__deepcopy__()
                move = TakeOffMovement(color, die_1, starting_loc)
                move.apply(scratch)
                move_node = Node(move, parent=root)
                distance_dict = update_distance_dict(die_1, distance_dict)
                new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                getMovesForDoubles(scratch, color, distance_dict, new_start, move_node)
            except IllegalMoveException:
                try:
                    scratch = board.__deepcopy__()
                    move = NormalMovement(color, die_1, starting_loc, starting_loc + die_1 * getDirection(color))
                    move.apply(scratch)
                    # apply die 1
                    move_node = Node(move, parent=root)
                    distance_dict_1 = update_distance_dict(die_1, distance_dict)
                    new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                    getMovesForDoubles(scratch, color, distance_dict_1, new_start, move_node)
                except IllegalMoveException:
                    pass

            if die_1 != die_2:
                try:
                    scratch = board.__deepcopy__()
                    move = TakeOffMovement(color, die_2, starting_loc)
                    move.apply(scratch)
                    move_node = Node(move, parent=root)
                    distance_dict = update_distance_dict(die_2, distance_dict)
                    new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                    getMovesForDoubles(scratch, color, distance_dict, new_start, move_node)
                except IllegalMoveException:
                    try:
                        scratch = board.__deepcopy__()
                        move = NormalMovement(color, die_2, starting_loc, starting_loc + die_2 * getDirection(color))
                        move.apply(scratch)
                        # apply die 2
                        move_node = Node(move, parent=root)
                        distance_dict_1 = update_distance_dict(die_2, distance_dict)
                        new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                        getMovesForDoubles(scratch, color, distance_dict_1, new_start, move_node)
                    except IllegalMoveException:
                        pass

            # don't apply either
            more_start = get_next_location_move_on(board.getCheckers(color), starting_loc, color)
            getMovesForDoubles(board, color, distance_dict, more_start, root)

    # All other cases: only normal moves remain
    else:
        die_1 = max(distance_dict)
        die_2 = min(distance_dict)
        try:
            scratch = board.__deepcopy__()
            move = NormalMovement(color, die_1, starting_loc, starting_loc + die_1 * getDirection(color))
            move.apply(scratch)
            # apply die 1
            move_node = Node(move, parent=root)
            distance_dict_1 = update_distance_dict(die_1, distance_dict)
            new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
            getMovesForDoubles(scratch, color, distance_dict_1, new_start, move_node)
        except IllegalMoveException:
            pass

        if die_1 != die_2:
            try:
                # apply die 2 if different
                scratch = board.__deepcopy__()
                move = NormalMovement(color, die_2, starting_loc, starting_loc + die_2 * getDirection(color))
                move.apply(scratch)
                # apply die 2
                move_node = Node(move, parent=root)
                distance_dict_1 = update_distance_dict(die_2, distance_dict)
                new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                getMovesForDoubles(scratch, color, distance_dict_1, new_start, move_node)

            except IllegalMoveException:
                pass

        # don't apply either
        more_start = get_next_location_move_on(board.getCheckers(color), starting_loc, color)
        getMovesForDoubles(board, color, distance_dict, more_start, root)
    return root


def generateMoves2(board: Board, color: str, dice: Dice, verbose=False):
    root = Node("root")
    getMovesForDoubles(board, color, dice.getDistances(), board.farthestBack(color), root)
    if verbose:
        print(board)
        print(dice)
        print(RenderTree(root).by_attr())
    height = root.height
    # TODO: where they can use either die but not both, use larger
    return tuple(PreOrderIter(root, filter_=lambda node: node.is_leaf and node.depth == height))


def time():
    b = Board()
    d = Dice()
    for i in range(1000):
        print(i)
        ms = generateMoves2(b, "BLACK", d, verbose=False)
        d.roll()


# cProfile.run('time()')

m = generateMoves2(Board(), "BLACK", Dice(2, 2), verbose=True)
print(len(m))
