from board.Board import getOtherColor, getRelativePointLocation, getScratch, getDirection, Board
from move.IllegalMoveException import IllegalMoveException
from move.Move import BarMovement, TakeOffMovement, NormalMovement


def update_distance_dict(die, distance_dict: dict):
    if die not in distance_dict:
        raise Exception("BAD!")

    distance_dict[die] = distance_dict[die] - 1
    if distance_dict[die] == 0:
        distance_dict.pop(die)


def getMovesForDoubles(board, color, distance_dict, starting_loc):
    result = set()

    # BASE CASES
    if not distance_dict:
        return result

    if not board.getCheckers(color):
        return result

    # if starting_loc < 1 or starting_loc > 24:
    #     return []

    #############################################

    # Pieces on bar
    if board.numBar(color) > 0:
        for die in distance_dict:
            if board.numAt(getOtherColor(color), getRelativePointLocation(getOtherColor(color), die)) <= 1:
                scratch = getScratch(board)
                try:
                    move = BarMovement(color, die, getRelativePointLocation(getOtherColor(color), die))
                    move.apply(scratch)
                    update_distance_dict(die, distance_dict)
                    rest = getMovesForDoubles(scratch, color, distance_dict, board.farthestBack(color))
                    return [move] + rest
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
                update_distance_dict(largest_die, distance_dict)
                rest = getMovesForDoubles(scratch, color, distance_dict, board.farthestBack(color))
                return [move] + rest
            except IllegalMoveException:
                pass

        else:
            for location in board.getCheckers(color):  # could start at starting_loc
                for die in distance_dict:
                    try:
                        scratch = getScratch(board)
                        move = TakeOffMovement(color, die, getRelativePointLocation(color, die))
                        move.apply(scratch)
                        update_distance_dict(die, distance_dict)
                        rest = getMovesForDoubles(scratch, color, distance_dict, location)
                        return [move] + rest
                    except IllegalMoveException:
                        try:
                            scratch = getScratch(board)
                            move = NormalMovement(color, die, location, location+die*getDirection(color))
                            move.apply(scratch)
                            update_distance_dict(die, distance_dict)
                            rest = getMovesForDoubles(scratch, color, distance_dict, location)
                            return [move] + rest
                        except IllegalMoveException:
                            pass
    #  Other
    else:
        for location in board.getCheckers(color):  # could start at starting_loc
            for die in distance_dict:
                try:
                    scratch = getScratch(board)
                    move = NormalMovement(color, die, location, location + die * getDirection(color))
                    move.apply(scratch)
                    update_distance_dict(die, distance_dict)
                    rest = getMovesForDoubles(scratch, color, distance_dict, location)
                    return [move] + rest
                except IllegalMoveException:
                    pass


b = Board()
print(getMovesForDoubles(b, "BLACK", {1:1, 3:1}, 1))