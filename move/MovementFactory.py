from itertools import permutations
from board.Board import getDirection, getScratch, getRelativePointLocation, getOtherColor, Board
from move.IllegalMoveException import IllegalMoveException
from move.Move import NormalMovement, Move, BarMovement, TakeOffMovement


def generate_moves(board, color, dice):
    locations = board.getCheckerSet(color)
    moves = []
    if not dice.isDoubles():

        combos = permutations(locations, 2)
        bad_first_die = set()
        bad_second_die = set()
        for combo in combos:
            if combo[0] not in bad_first_die and combo[1] not in bad_second_die:
                first = buildMovement(board, color, dice.getDie1(), combo[0], return_board=True)
                if first:
                    first_movement, board_after = first
                    second_movement = buildMovement(board_after, color, dice.getDie2(), combo[1])
                    if second_movement:
                        moves.append(Move(color, dice, [first_movement, second_movement]))
                    else:
                        bad_second_die.add(combo[1])
                else:
                    bad_first_die.add(combo[0])

        #  ADDITIONAL MOVE TWICE OPTIONS (can only work if no pieces on bar)
        if (board.numBar(color)) == 0:
            for point in locations - (bad_first_die & bad_second_die):
                # -------------------------------------------------------------------------------------------
                # ONE MOVES TWICE
                if point in bad_first_die:
                    if board.numAt(color, point+dice.getDie2()*getDirection(color)) == 0:  # Check to not make dup. move
                        first = buildMovement(board, color, dice.getDie2(), point, return_board=True)
                        if first:
                            first_movement, board_after = first
                            second = buildMovement(board_after, color, dice.getDie1(), point+dice.getDie2()*getDirection(color))
                            if second:
                                moves.append(Move(color, dice, [first_movement, second]))
                elif point in bad_second_die:
                    if board.numAt(color, point+dice.getDie1()*getDirection(color)) == 0:
                        first = buildMovement(board, color, dice.getDie1(), point, return_board=True)
                        if first:
                            first_movement, board_after = first
                            second = buildMovement(board_after, color, dice.getDie2(), point+dice.getDie1()*getDirection(color))
                            if second:
                                moves.append(Move(color, dice, [first_movement, second]))
                else:
                    # TODO: sometimes order might matter here (if hitting someone)
                    if board.numAt(color, point+dice.getDie1()*getDirection(color)) == 0:
                        first = buildMovement(board, color, dice.getDie1(), point, return_board=True)
                        if first:
                            first_movement, board_after = first
                            second = buildMovement(board_after, color, dice.getDie2(),
                                                   point + dice.getDie1() * getDirection(color))
                            if second:
                                moves.append(Move(color, dice, [first_movement, second]))
                        # Order may matter if they hit with previous move
                        if board.numAt(getOtherColor(color), point+dice.getDie1()*getDirection(color)) != 0:
                            first = buildMovement(board, color, dice.getDie2(), point, return_board=True)
                            if first:
                                first_movement, board_after = first
                                second = buildMovement(board_after, color, dice.getDie1(),
                                                       point + dice.getDie2() * getDirection(color))
                                if second:
                                    moves.append(Move(color, dice, [first_movement, second]))

                # _________________________________________________________________________________________
                # TWO MOVE FROM SAME POINT
                if point not in bad_first_die and point not in bad_second_die and board.numAt(color, point) > 1:
                    first = buildMovement(board, color, dice.getDie1(), point)
                    second = buildMovement(board, color, dice.getDie2(), point)
                    if not (first and second):
                        print("UNEXPECTED ERROROR")
                    moves.append(Move(color, dice, [first, second]))

    else:
        # TODO: this could be made faster
        pass
    print(str(len(moves)) + " moves: ", end="")
    print(moves)

    return moves


def buildMovement(board, color, die, location, return_board=False):
    scratch = getScratch(board)
    try:
        move = BarMovement(color, die, getRelativePointLocation(color, die))
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
            except IllegalMoveException:
                return False  # the die cannot be applied to this location given the board


# def sameResult(board: Board, move1: Move, move2: Move):
#     board1 = getScratch(board)
#     move1.apply(board1, check="minimal")
#     board2 = getScratch(board)
#     move2.apply(board2, check="minimal")
#     return board1 == board2
