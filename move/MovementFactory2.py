from itertools import combinations
from board.Board import getDirection, getScratch, getRelativePointLocation, getOtherColor, Board
from move.IllegalMoveException import IllegalMoveException
from move.Move import NormalMovement, Move, BarMovement, TakeOffMovement


def generate_moves(board, color, dice):
    locations = board.getCheckerSet(color)
    moves = set()
    if not dice.isDoubles():
        # TODO: legal move once
        #
        #  MOVE TWO FROM SEPARATE POINTS
        combos = combinations(locations, 2)
        for combo in combos:
            first = buildMovement(board, color, dice.getDie1(), combo[0], return_board=True)
            if first:
                first_movement, board_after = first
                second_movement = buildMovement(board_after, color, dice.getDie2(), combo[1])
                if second_movement:
                    moves.add(Move(board, color, dice, [first_movement, second_movement]))

            first = buildMovement(board, color, dice.getDie2(), combo[0], return_board=True)
            if first:
                first_movement, board_after = first
                second_movement = buildMovement(board_after, color, dice.getDie1(), combo[1])
                if second_movement:
                    moves.add(Move(board, color, dice, [first_movement, second_movement]))

        #  ADDITIONAL MOVE TWICE OPTIONS (can only work if no pieces on bar)
        if (board.numBar(color)) == 0:
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

    else:
        # TODO: do this
        pass
    print(str(len(moves)) + " moves: ", end="")
    print(moves)
    
    for move in moves:
        if move.getBoardAfter() is None:
            print("BAD MOVE " + str(move))

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
            except IllegalMoveException:
                return False  # the die cannot be applied to this location given the board

#
# def sameResult(board: Board, move1: Move, move2: Move):
#     board1 = getScratch(board)
#     move1.apply(board1, check="minimal")
#     board2 = getScratch(board)
#     move2.apply(board2, check="minimal")
#     return board1 == board2
