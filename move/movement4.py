from copy import copy
from anytree import Node

from board.Board import getOtherColor, getRelativePointLocation, getScratch, getDirection, Board
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


def getMovesForDoubles(board, color, distance_dict, starting_loc):
    result = []

    # BASE CASES
    if not distance_dict:
        return []

    if not starting_loc:
        return []

    #############################################

    # Pieces on bar
    if board.numBar(color) > 0:
        for die in distance_dict:
            if board.numAt(getOtherColor(color), getRelativePointLocation(getOtherColor(color), die)) <= 1:
                scratch = getScratch(board)
                try:
                    move = BarMovement(color, die, getRelativePointLocation(getOtherColor(color), die))
                    move.apply(scratch)
                    result.append(move)
                    distance_dict = update_distance_dict(die, distance_dict)
                    rest = getMovesForDoubles(scratch, color, distance_dict, board.farthestBack(color))
                    result.extend(rest)
                except IllegalMoveException:
                    pass
        return []

    # Able to bear off
    elif board.allInHome(color):
        largest_die = max(distance_dict)
        if largest_die >= getRelativePointLocation(color, board.farthestBack(color)):
            scratch = getScratch(board)
            try:
                move = TakeOffMovement(color, largest_die, board.farthestBack(color))
                move.apply(scratch)
                result.append(move)
                distance_dict = update_distance_dict(largest_die, distance_dict)
                rest = getMovesForDoubles(scratch, color, distance_dict, board.farthestBack(color))
                result.extend(rest)
            except IllegalMoveException:
                pass

        else:
            for die in distance_dict:
                try:
                    scratch = getScratch(board)
                    move = TakeOffMovement(color, die, getRelativePointLocation(color, die))
                    move.apply(scratch)
                    result.append(move)
                    distance_dict = update_distance_dict(die, distance_dict)
                    rest = getMovesForDoubles(scratch, color, distance_dict, board.farthestBack(color))
                    result.extend(rest)
                except IllegalMoveException:
                    try:
                        scratch = getScratch(board)
                        move = NormalMovement(color, die, starting_loc, starting_loc+die*getDirection(color))
                        move.apply(scratch)
                        result.append(move)
                        distance_dict = update_distance_dict(die, distance_dict)
                        new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                        rest = getMovesForDoubles(scratch, color, distance_dict, new_start)
                        result.extend(rest)
                    except IllegalMoveException:
                        pass
    #  Other
    else:
        die_1 = max(distance_dict)
        die_2 = min(distance_dict)
        try:
            scratch = getScratch(board)
            move = NormalMovement(color, die_1, starting_loc, starting_loc + die_1 * getDirection(color))
            move.apply(scratch)
            # apply die 1
            distance_dict_1 = update_distance_dict(die_1, distance_dict)
            new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
            rests = getMovesForDoubles(scratch, color, distance_dict_1, new_start)
            moves = [move]
            moves.extend(rests)
            result.append(moves)
            # apply die 2 if different
            if die_1 != die_2 and board.numAt(getOtherColor(color), starting_loc + die_1 * getDirection(color)) == 1:
                try:
                    scratch = getScratch(board)
                    move = NormalMovement(color, die_2, starting_loc, starting_loc + die_2 * getDirection(color))
                    move.apply(scratch)
                    # apply die 2
                    distance_dict_1 = update_distance_dict(die_2, distance_dict)
                    new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                    rests = getMovesForDoubles(scratch, color, distance_dict_1, new_start)
                    moves = [move]
                    moves.extend(rests)
                    result.append(moves)
                except IllegalMoveException:
                    pass
        except IllegalMoveException:
            if die_1 != die_2:
                try:
                    scratch = getScratch(board)
                    move = NormalMovement(color, die_2, starting_loc, starting_loc + die_2 * getDirection(color))
                    move.apply(scratch)
                    # apply die 2
                    distance_dict_1 = update_distance_dict(die_2, distance_dict)
                    new_start = get_next_location(scratch.getCheckers(color), starting_loc, color)
                    rests = getMovesForDoubles(scratch, color, distance_dict_1, new_start)
                    moves = [move]
                    moves.extend(rests)
                    result.append(moves)
                except IllegalMoveException:
                    pass

        # don't apply either
        more_start = get_next_location_move_on(board.getCheckers(color), starting_loc, color)
        more = getMovesForDoubles(board, color, distance_dict, more_start)
        result.extend(more)
    return result


def time():
    b = Board()
    print(getMovesForDoubles(b, "BLACK", {1: 4}, b.farthestBack('BLACK')))


# cProfile.run('time()')

b = Board()
print(b)
mooves = getMovesForDoubles(b, "BLACK", {1: 4}, b.farthestBack('BLACK'))
print(mooves)
