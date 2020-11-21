from move.IllegalMoveException import IllegalMoveException
from board.Board import getDirection, getOtherColor, getRelativePointLocation, getScratch
# TODO: project: add argument types to classes


def createFromString(text, color, board, dice):
    movements = []
    str_list = text.split(" ")
    for i in range(len(str_list)):
        move_str = str_list[i]
        try:
            [start_str, end_str] = move_str.split("/")
        except ValueError:
            print("Wasn't able to process move input (eg. bar/3 3/12 or 17/18 19/off)")
            return False
        if "bar" == start_str:
            end = int(end_str)
            die = getRelativePointLocation(getOtherColor(color), end)
            movements.append(BarMovement(color, die, end))
        elif "off" == end_str:
            start = int(start_str)
            if getRelativePointLocation(color, start) in dice.getDice():
                die = getRelativePointLocation(color, start)
            else:  # figure out which die to apply to taking off move
                if board.allInHome(color):
                    die = max(dice.getDice()) if i == 0 else min(dice.getDice())
                else:
                    try:
                        die = dice.getDie1() if dice.getDie2() == used_die else dice.getDie2()
                    except NameError:
                        print("You must move pieces in before taking off")
                        return False

            movements.append(TakeOffMovement(color, die, start))
        else:
            start = int(start_str)
            end = int(end_str)
            die = abs(end - start)
            used_die = die
            movements.append(NormalMovement(color, die, start, end))

    move = Move(board, color, dice, movements)
    if move.getBoardAfter():
        return Move(board, color, dice, movements)
    else:
        return False


class NormalMovement:

    def __init__(self, color, die, start, end):
        self.color = color
        self.die = die
        self.start = start
        self.end = end
        if (not (1 <= self.start <= 24)) or (not (1 <= self.end <= 24)):
            raise IllegalMoveException("Invalid location")

    def getEnd(self):
        return self.end

    def getDieUsed(self):
        return self.die

    def apply(self, board):
        if abs(self.end - self.start) != self.die:
            raise IllegalMoveException("Move cannot be made given the die value " + str(self.die))

        if board.numBar(self.color) > 0:
            raise IllegalMoveException("You must move from the bar first")

        if board.numAt(self.color, self.start) == 0:
            raise IllegalMoveException("You don't have enough pieces at the start " + str(self.start))

        if (self.start > self.end and getDirection(self.color) > 0) or (
                self.start < self.end and getDirection(self.color) < 0):
            raise IllegalMoveException("You can't move backwards")

        if board.numAt(getOtherColor(self.color), self.end) > 1:
            raise IllegalMoveException("Other player occupies point " + str(self.end))

        # VALID MOVEMENT, check if hit
        if board.numAt(getOtherColor(self.color), self.end) == 1:
            board.removeFromLocation(getOtherColor(self.color), self.end)
            board.moveToBar(getOtherColor(self.color))

        board.removeFromLocation(self.color, self.start)
        board.moveToLocation(self.color, self.end)

    def __str__(self):
        return str(self.start) + "/" + str(self.end)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return type(self) == type(
            other) and self.start == other.start and self.end == other.end and self.color == other.color


class BarMovement:

    def __init__(self, color, die, end):
        self.color = color
        self.die = die
        self.end = end
        if not (1 <= self.end <= 24):
            raise IllegalMoveException("Invalid location")

    def getEnd(self):
        return self.end

    def getDieUsed(self):
        return self.die

    def apply(self, board):
        if self.die != getRelativePointLocation(getOtherColor(self.color), self.end):
            raise IllegalMoveException("Move cannot be made given the die value " + str(self.die))

        if board.numBar(self.color) == 0:
            raise IllegalMoveException("Must have pieces on bar")

        if board.numAt(getOtherColor(self.color), self.end) > 1:
            raise IllegalMoveException("Other player occupies the location " + str(self.end))

        # VALID MOVEMENT, check if hit
        if board.numAt(getOtherColor(self.color), self.end) == 1:
            board.removeFromLocation(getOtherColor(self.color), self.end)
            board.moveToBar(getOtherColor(self.color))

        board.moveFromBar(self.color)
        board.moveToLocation(self.color, self.end)

    def __str__(self):
        return "bar/" + str(self.end)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return type(self) == type(other) and self.end == other.end and self.color == other.color


class TakeOffMovement:

    def __init__(self, color, die, start):
        self.color = color
        self.die = die
        self.start = start
        if not (1 <= self.start <= 24):
            raise IllegalMoveException("Invalid location")

    def getEnd(self):
        return False

    def getDieUsed(self):
        return self.die

    def apply(self, board):
        if board.numAt(self.color, self.start) == 0:
            raise IllegalMoveException("You don't have enough pieces at the start " + str(self.start))

        if not board.allInHome(self.color):
            raise IllegalMoveException("You must have all your pieces in home before taking off")

        if getRelativePointLocation(self.color, self.start) > self.die:
            raise IllegalMoveException("Move cannot be made given the die value " + str(self.die))
        elif getRelativePointLocation(self.color, self.start) < self.die:
            if board.farthestBack(self.color) != self.start:
                raise IllegalMoveException("You must move the farthest back piece off that you can with die " + str(self.die))

        # VALID MOVEMENT
        board.removeFromLocation(self.color, self.start)
        board.moveOff(self.color)

    def __str__(self):
        return str(self.start) + "/off"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return type(self) == type(other) and self.start == other.start and self.color == other.color


class Move:

    def __init__(self, board_before, color, dice, movements, board_after):
        self.color = color
        self.dice = dice
        self.movements = movements
        self.board_before = board_before
        self.board_after = board_after
        if dice.isDoubles():
            self.distances = [dice.getDie1()] * 4
        else:
            self.distances = [dice.getDie1(), dice.getDie2()]

        # if movements != "empty":
        #     try:
        #         self.apply()
        #     except IllegalMoveException as e:
        #         print(e)
        # else:
        #     self.board_after = self.board_before

    def __str__(self):
        strg = self.color
        for movement in self.movements:
            strg += " " + str(movement)
        return strg

    def __repr__(self):
        return str(self)

    def setBoardAfter(self, board_after):
        self.board_after = board_after

    def getBoardAfter(self):
        return self.board_after

    def apply(self):
        #  Check that the moves use the given dice
        # distances = self.distances
        # for movement in self.movements:
        #     try:
        #         distances.remove(movement.getDieUsed())
        #     except ValueError:
        #         raise IllegalMoveException("Move cannot be made given the dice")
        #
        # #  Test to make sure a player used all of their dice that they could
        # #  TODO: sometimes a player can move either die but not both (rules say must use larger)
        # #  TODO: sometimes a player can move some doubles but not all
        # if len(distances) > 0:
        #     for die in distances:
        #         if self.canMove(die):
        #             raise IllegalMoveException("You must use all of your dice")

        #  Test if all moves are valid
        scratch = getScratch(self.board_before)
        for movement in self.movements:
            movement.apply(scratch)

        # NOW VALID MOVE, APPLY MOVEMENTS
        self.board_after = scratch

    def canMove(self, die):
        scratch = getScratch(self.board_before)

        #  Can they move from the bar
        try:
            move = BarMovement(self.color, die, getRelativePointLocation(getOtherColor(self.color), die))
            move.apply(scratch)
            return True
        except IllegalMoveException:
            pass

        locations = scratch.getCheckerSet(self.color)
        for location in locations:
            #  Can they move normally
            try:
                move = NormalMovement(self.color, die, location, location+die*getDirection(self.color))
                move.apply(scratch)
                return True
            except IllegalMoveException:
                pass

            #  Can they take off a piece
            try:
                move = TakeOffMovement(self.color, die, location)
                move.apply(scratch)
                return True
            except IllegalMoveException:
                pass
        return False

    def __hash__(self):
        if self.board_after is None:
            raise NameError("No Board after")
        return hash(self.board_after)

    def __eq__(self, other):
        if type(self) == type(other):
            if self.board_after is not None and other.board_after is not None:
                board_stuff = self.board_after == other.board_after
            else:
                raise NameError("Board after has not been initalized by one of the two moves")
            return self.color == other.color and board_stuff
        else:
            return False
