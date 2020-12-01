from board.Board import NONE, getOtherColor, getDirection


def export(backgammon):
    current_color = backgammon.players[backgammon.on_roll].color
    double_possession = backgammon.board.doublePossession
    direction = getDirection(current_color)

    string = ""

    match_length = 0
    string += str(match_length) + ";"

    jacoby = 0
    string += str(jacoby) + ";0;1;"

    current_player = backgammon.on_roll
    string += str(current_player) + ";"

    name_0, name_1 = backgammon.players[0].color, backgammon.players[1].color
    string += str(name_1) + ";gnubg;"

    crawford = 0
    string += str(crawford) + ";"

    score_0, score_1 = 0, 0
    string += str(score_0) + ";" + str(score_1) + ";"

    cube_value = backgammon.board.doubleCube
    string += str(cube_value) + ";"

    cube_possesion = 0 if double_possession == NONE else 1 if double_possession == current_color else -1
    string += str(cube_possesion) + ";"

    current_on_bar = backgammon.board.numBar(current_color)
    string += str(current_on_bar) + ";"

    points = backgammon.board.pointsContent[1:-1] if direction == -1 else reversed(backgammon.board.pointsContent[1:-1])
    points = [direction*point for point in points]
    for point in points:
        string += str(point) + ";"

    other_on_bar = backgammon.board.numBar(getOtherColor(current_color))
    string += str(other_on_bar) + ";"

    die_1, die_2 = backgammon.dice.die1, backgammon.dice.die2
    string += str(die_1) + ";" + str(die_2) + ";"

    return string
