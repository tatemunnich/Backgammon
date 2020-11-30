from board.Board import getOtherColor, Board, BLACK, NONE
from board.Dice import Dice
from move.MovementFactory import generate_boards

probability = {
    (1, 1): 1 / 36, (2, 1): 2 / 36, (3, 1): 2 / 36, (4, 1): 2 / 36, (5, 1): 2 / 36, (6, 1): 2 / 36,
    (2, 2): 1 / 36, (2, 3): 2 / 36, (2, 4): 2 / 36, (2, 5): 2 / 36, (2, 6): 2 / 36,
    (3, 3): 1 / 36, (3, 4): 2 / 36, (3, 5): 2 / 36, (3, 6): 2 / 36,
    (4, 4): 1 / 36, (4, 5): 2 / 36, (4, 6): 2 / 36,
    (5, 5): 1 / 36, (5, 6): 2 / 36,
    (6, 6): 1 / 36
}


def get_board_children(board, dice=None):
    if not dice:
        children = {}
        for roll in probability:
            moves = generate_boards(board, board.turn, Dice(roll[0], roll[1]))
            children[roll] = moves
    else:
        return generate_boards(board, board.turn, dice)
    return children


def h(board, color):
    points = board.getCheckers(color)
    home = 25 if color == BLACK else 0
    pips = 0
    for point in points:
        num_at = board.pointsContent[point]
        if num_at == 1:
            pips += num_at * (home - point)  # maybe treat blots differently
        else:
            pips += num_at * (home - point)
    pips += 25 * board.numBar(color)
    return pips


def expectiminimax(board, ply, color, dice=None):
    if ply > 2:
        raise Exception("don't do more than 2")

    if board.getWinner() != NONE or ply == 0:
        return h(board, color)

    if board.turn == color and dice:
        alpha = 375
        children = get_board_children(board, dice)
        for new_board in children:
            alpha = min(alpha, expectiminimax(new_board, ply-1, color))

    elif board.turn == getOtherColor(color) and not dice:
        roll_dict = get_board_children(board)
        alpha = 0
        for roll in roll_dict:
            roll_alpha = 0
            for new_board in roll_dict[roll]:
                roll_alpha = max(roll_alpha, expectiminimax(new_board, ply-1, color))
                if roll == (1,1):
                    print(roll)
                    print(new_board)
                    print(expectiminimax(new_board, ply-1, color))
                    print()
            if roll == (1,1):
                print("FINAL ROLLALPHA")
                print(roll_alpha)
            alpha = alpha + roll_alpha * probability[roll]

    else:
        raise Exception("shouldn't get here")

    return alpha


b = Board()

print(expectiminimax(b, 1, BLACK, Dice(5, 1)))
