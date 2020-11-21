from itertools import permutations
from board.Board import getDirection, getScratch, getRelativePointLocation, getOtherColor, Board
from move.IllegalMoveException import IllegalMoveException
from move.Move import NormalMovement, Move, BarMovement, TakeOffMovement


def generate_moves(board, color, dice):
    locations = board.getCheckerSet(color)
    moves = set()
    if not dice.isDoubles():
        bad_first_die = set()
        bad_second_die = set()
        #  MOVE TWO FROM SEPARATE POINTS
        combos = permutations(locations, 2)
        for combo in combos:
            first = buildMovement(board, color, dice.getDie1(), combo[0], return_board=True)
            if first:
                first_movement, board_after = first
                second_movement = buildMovement(board_after, color, dice.getDie2(), combo[1])
                if second_movement:
                    moves.add(Move(board, color, dice, [first_movement, second_movement]))
                else:
                    bad_second_die.add(combo[1])
            else:
                bad_first_die.add(combo[0])

            first = buildMovement(board, color, dice.getDie2(), combo[0], return_board=True)
            if first:
                first_movement, board_after = first
                second_movement = buildMovement(board_after, color, dice.getDie1(), combo[1])
                if second_movement:
                    moves.add(Move(board, color, dice, [first_movement, second_movement]))
                else:
                    bad_second_die.add(combo[1])
            else:
                bad_first_die.add(combo[0])

        # ONE COMES IN AND MOVES AGAIN
        num_bar = board.numBar(color)
        if num_bar == 1:
            first = buildMovement(board, color, dice.getDie1(), -1, return_board=True)
            if first:
                first_movement, board_after = first
                second = buildMovement(board_after, color, dice.getDie2(),
                                       getRelativePointLocation(getOtherColor(color), dice.getDie1()))
                if second:
                    moves.add(Move(board, color, dice, [first_movement, second]))

            first = buildMovement(board, color, dice.getDie2(), -1, return_board=True)
            if first:
                first_movement, board_after = first
                second = buildMovement(board_after, color, dice.getDie1(),
                                       getRelativePointLocation(getOtherColor(color), dice.getDie2()))
                if second:
                    moves.add(Move(board, color, dice, [first_movement, second]))

        #  ADDITIONAL MOVE TWICE OPTIONS (can only work if no pieces on bar)
        if num_bar == 0:
            for point in locations:
                # -------------------------------------------------------------------------------------------
                # ONE MOVES TWICE
                first = buildMovement(board, color, dice.getDie1(), point, return_board=True)
                if first:
                    first_movement, board_after = first
                    second = buildMovement(board_after, color, dice.getDie2(),
                                           point + dice.getDie1() * getDirection(color))
                    if second:
                        moves.add(Move(board, color, dice, [first_movement, second]))

                first = buildMovement(board, color, dice.getDie2(), point, return_board=True)
                if first:
                    first_movement, board_after = first
                    second = buildMovement(board_after, color, dice.getDie1(),
                                           point + dice.getDie2() * getDirection(color))
                    if second:
                        moves.add(Move(board, color, dice, [first_movement, second]))
                # _________________________________________________________________________________________
                # TWO MOVE FROM SAME POINT
                if board.numAt(color, point) > 1:
                    first = buildMovement(board, color, dice.getDie1(), point)
                    if first:
                        second = buildMovement(board, color, dice.getDie2(), point)
                        if second:
                            moves.add(Move(board, color, dice, [first, second]))

        # can move once or zero times
        if len(moves) == 0:
            other_color = getOtherColor(color)
            if num_bar > 1:
                come_in_1 = not board.numAt(other_color, getRelativePointLocation(other_color, dice.getDie1())) > 1
                come_in_2 = not board.numAt(other_color, getRelativePointLocation(other_color, dice.getDie2())) > 1
                if not (come_in_1 or come_in_2):
                    moves.add(Move(board, color, dice, "empty"))
                    return moves
                elif not come_in_1:
                    first_movement = buildMovement(board, color, dice.getDie2(), -1)  # location doesn't matter for coming in
                    moves.add(Move(board, color, dice, [first_movement]))
                    return moves
                elif not come_in_2:
                    first_movement = buildMovement(board, color, dice.getDie1(), -1)  # location doesn't matter for coming in
                    moves.add(Move(board, color, dice, [first_movement]))
                    return moves

            if num_bar == 1:
                come_in_1 = not board.numAt(other_color, getRelativePointLocation(other_color, dice.getDie1())) > 1
                come_in_2 = not board.numAt(other_color, getRelativePointLocation(other_color, dice.getDie2())) > 1
                if not (come_in_1 or come_in_2):
                    moves.add(Move(board, color, dice, "empty"))
                    return moves

            # 1 or 0 on bar
            # TODO just can't move one of the die at all

    else:
        # TODO: do this
        pass
    print(str(len(moves)) + " moves: ", end="")
    print(moves)
    
    for move in moves:
        if move.getBoardAfter() is None:
            raise Exception("BAD MOVE")

    return moves


def buildMovement(board, color, die, location, return_board=False):
    scratch = getScratch(board)
    try:
        move = BarMovement(color, die, getRelativePointLocation(getOtherColor(color), die))
        move.apply(scratch)
        if return_board:
            return move, scratch  # end function because piece on the bar so no other options
        else:
            return move
    except IllegalMoveException:
        #  Can they move normally
        try:
            move = NormalMovement(color, die, location, location+die*getDirection(color))
            move.apply(scratch)
            if return_board:
                return move, scratch
            else:
                return move
        except IllegalMoveException:
            # Can they take off a piece (you can't move normally AND take off same piece with same die)
            try:
                move = TakeOffMovement(color, die, location)
                move.apply(scratch)
                if return_board:
                    return move, scratch
                else:
                    return move
            except IllegalMoveException as e:
                return False  # the die cannot be applied to this location given the board


# This may be obsolete, but should look at bottom section for logic
def canMove(board, color, dice, dienumber):
    scratch = getScratch(board)
    if dienumber == 1:
        die = dice.getDie1()
        other_die = dice.getDie2()
    elif dienumber == 2:
        die = dice.getDie2()
        other_die = dice.getDie1()
    else:
        raise Exception("Invalid input to canMove function for dienumber")

    #  Can they move from the bar
    try:
        move = BarMovement(color, die, getRelativePointLocation(getOtherColor(color), die))
        move.apply(scratch)
        return True
    except IllegalMoveException:
        pass

    locations = scratch.getCheckerSet(color)
    for location in locations:
        #  Can they move normally
        try:
            move = NormalMovement(color, die, location, location+die*getDirection(color))
            move.apply(scratch)
            return True
        except IllegalMoveException:
            pass

        #  Can they take off a piece
        try:
            move = TakeOffMovement(color, die, location)
            move.apply(scratch)
            return True
        except IllegalMoveException:
            pass

    #  Maybe they can move die after moving the other die first
    if not dice.isDoubles():
        for location in locations:
            try:
                first = buildMovement(board, color, other_die, location, return_board=True)
                if first:
                    first_movement, board_after = first
                    second = buildMovement(board_after, color, die, first_movement.getEnd())
                    if second:
                        print("They can use die " + str(die) + " by doing " + str(first_movement) + " first.")
                        return True
            except IllegalMoveException:
                pass

    return False
