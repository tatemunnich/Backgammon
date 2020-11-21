from board.Board import getDirection, getScratch, getRelativePointLocation, getOtherColor, Board
from move.IllegalMoveException import IllegalMoveException
from move.Move import NormalMovement, Move, BarMovement, TakeOffMovement


def generate_moves(board, color, dice, verbose=False):
    moves = set()
    initial_locations = board.getCheckerSet(color)
    die_1 = dice.getDie1()
    die_2 = dice.getDie2()
    can_move_1_first = False
    can_move_2_first = False
    can_move_1_second = False
    can_move_2_second = False
    for location in initial_locations:
        first_1 = buildMovement(board, color, die_1, location)
        if first_1:
            can_move_1_first = True
            first_movement_1, board_after_1 = first_1
            # print("first move1 would work: " + str(first_movement_1))
            locations_1 = board_after_1.getCheckerSet(color)
            if len(locations_1) == 0:
                moves.add(Move(board, color, dice, [first_movement_1], board_after_1))
                return moves
            for location_1 in locations_1:
                second_1 = buildMovement(board_after_1, color, die_2, location_1)
                # print(second_movement_1)
                if second_1:
                    second_movement_1, board_after_1_2 = second_1
                    can_move_2_second = True
                    # print("trying to add move " + str(Move(board, color, dice, [first_movement_1, second_movement_1])))
                    moves.add(Move(board, color, dice, [first_movement_1, second_movement_1], board_after_1_2))

        first_2 = buildMovement(board, color, die_2, location)
        if first_2:
            can_move_2_first = True
            first_movement_2, board_after_2 = first_2
            # print("first move2 would work: " + str(first_movement_2))
            locations_2 = board_after_2.getCheckerSet(color)
            if len(locations_2) == 0:
                moves.add(Move(board, color, dice, [first_movement_2], board_after_2))
                return moves
            for location_2 in locations_2:
                second_2 = buildMovement(board_after_2, color, die_1, location_2)
                if second_2:
                    second_movement_2, board_after_2_1 = second_2
                    can_move_1_second = True
                    # print("trying to add move " + str(Move(board, color, dice, [first_movement_2, second_movement_2])))
                    moves.add(Move(board, color, dice, [first_movement_2, second_movement_2], board_after_2_1))

    if len(moves) == 0:
        if not (can_move_1_first or can_move_2_first):
            moves.add(Move(board, color, dice, [], board))
        elif can_move_1_first and not can_move_2_second and not can_move_2_first:
            #  Legal to move only the first die
            for location in initial_locations:
                first = buildMovement(board, color, die_1, location)
                if first:
                    first_movement, board_after = first
                    moves.add(Move(board, color, dice, [first_movement], board_after))
        elif can_move_2_first and not can_move_1_second and not can_move_1_first:
            #  Legal to move only the second die
            for location in initial_locations:
                first = buildMovement(board, color, die_2, location)
                if first:
                    first_movement, board_after = first
                    moves.add(Move(board, color, dice, [first_movement], board_after))
        elif can_move_1_first and not can_move_2_second and can_move_2_first and not can_move_1_second:
            #  Legal to move only the first die or only the second die but not both
            #  Move the larger of the two
            for location in initial_locations:
                first = buildMovement(board, color, max(dice.getDice()), location)
                if first:
                    first_movement, board_after = first
                    moves.add(Move(board, color, dice, [first_movement], board_after))

    if verbose:
        print(str(len(moves)) + " moves: ", end="")
        print(moves)
    return moves


def getLocationsForDoubles(board, color, die):
    locations = board.getCheckerSet(color)
    for location in locations:
        buildMovement(board, color, die, location)


def buildMovement(board, color, die, location):
    scratch = getScratch(board)
    try:
        move = BarMovement(color, die, getRelativePointLocation(getOtherColor(color), die))
        move.apply(scratch)
        return move, scratch  # end function because piece on the bar so no other options
    except IllegalMoveException:
        #  Can they move normally
        try:
            move = NormalMovement(color, die, location, location+die*getDirection(color))
            move.apply(scratch)
            return move, scratch
        except IllegalMoveException:
            # Can they take off a piece (you can't move normally AND take off same piece with same die)
            try:
                move = TakeOffMovement(color, die, location)
                move.apply(scratch)
                return move, scratch
            except IllegalMoveException:
                return False  # the die cannot be applied to this location given the board
