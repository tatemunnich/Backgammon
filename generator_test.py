import unittest

from board.Board import Board
from board.Dice import Dice
from move.MovementFactory import generate_moves


class MyTestCase(unittest.TestCase):

    def test_0(self):
        b = Board()
        d = Dice(5, 1)
        m = generate_moves(b, "BLACK", d)

        print(b)
        print(m)
        self.assertEqual(len(m), 8)
        # self.assertEqual(set([str(move) for move in m]), {"17/22 19/20", "12/17 19/20", "1/7", "1/2 12/17", "17/23",
        #                      "12/18", "1/2 17/22", "17/22 17/18"})

    def test_1(self):
        b = Board()
        b.pointsContent = [0] * 26
        b.pointsContent[1] = -2
        b.pointsContent[12] = -5
        b.pointsContent[17] = -3
        b.pointsContent[19] = -5
        b.pointsContent[2] = 14
        b.pointsContent[7] = 1
        b.whiteCheckers = {1, 12, 17, 19}
        b.blackCheckers = {2, 7}
        b.blackCheckersTaken = 0
        b.whiteCheckersTaken = 0

        d = Dice(5, 1)
        m = generate_moves(b, "BLACK", d)

        self.assertEqual(len(m), 1)
        # self.assertEqual(m, {"7/2"})

    def test_2(self):
        b = Board()
        b.pointsContent = [0] * 26
        b.pointsContent[1] = -1
        b.pointsContent[5] = -1
        b.pointsContent[12] = -5
        b.pointsContent[17] = -3
        b.pointsContent[19] = -5
        b.pointsContent[2] = 14
        b.pointsContent[7] = 1
        b.whiteCheckers = {1, 5, 12, 17, 19}
        b.blackCheckers = {2, 7}
        b.blackCheckersTaken = 0
        b.whiteCheckersTaken = 0

        d = Dice(1, 2)
        m = generate_moves(b, "BLACK", d)
        print(b)
        print(m)

        self.assertEqual(len(m), 4)
        # self.assertEqual(m, {"7/5 2/1", "7/6 2/off", "7/5 5/4", "7/6 6/4"})

    def test_3(self):
        b = Board()
        b.pointsContent = [0] * 26
        b.pointsContent[1] = -1
        b.pointsContent[12] = -6
        b.pointsContent[17] = -3
        b.pointsContent[19] = -5
        b.pointsContent[2] = 14
        b.pointsContent[7] = 1
        b.whiteCheckers = {1, 12, 17, 19}
        b.blackCheckers = {2, 7}
        b.blackCheckersTaken = 0
        b.whiteCheckersTaken = 0

        d = Dice(1, 2)
        m = generate_moves(b, "BLACK", d)
        print(b)
        print(m)

        self.assertEqual(len(m), 3)
        # self.assertEqual(m, {"7/5 2/1", "7/6 2/off", "7/5 5/4==7/6 6/4"})

    def test_4(self):
        b = Board()
        b.pointsContent = [0] * 26
        b.pointsContent[1] = -1
        b.pointsContent[2] = 2
        b.pointsContent[4] = 1
        b.pointsContent[5] = 1
        b.pointsContent[6] = 3
        b.pointsContent[8] = 1
        b.pointsContent[12] = -5
        b.pointsContent[13] = 5
        b.pointsContent[17] = -2
        b.pointsContent[19] = -4
        b.pointsContent[20] = -1
        b.pointsContent[22] = -1
        b.pointsContent[24] = 2
        b.whiteCheckers = {1, 12, 17, 19, 20, 22}
        b.blackCheckers = {24, 13, 8, 6, 5, 4, 2}
        b.whiteCheckersTaken = 1
        b.blackCheckersTaken = 0

        d = Dice(4, 2)
        m = generate_moves(b, "WHITE", d)
        print(b)
        print(m)

        self.assertEqual(len(m), 5)
        # self.assertEqual(m, {"bar/4 /1/3", "bar/4 12/14", "bar/4 17/19", "bar/4 19/21", "bar/4 20/22"})

    def test_5(self):
        b = Board()
        b.pointsContent = [0] * 26
        b.pointsContent[1] = -2
        b.pointsContent[12] = -5
        b.pointsContent[17] = -3
        b.pointsContent[19] = -5
        b.pointsContent[24] = 2
        b.pointsContent[13] = 5
        b.pointsContent[4] = 3
        b.pointsContent[6] = 5
        b.whiteCheckers = {12, 17, 19}
        b.blackCheckers = {24, 13, 6, 4}
        b.whiteCheckersTaken = 2
        b.blackCheckersTaken = 0

        d = Dice(4, 6)
        m = generate_moves(b, "WHITE", d)
        print(b)
        print(m)

        self.assertEqual(len(m), 1)
        # self.assertEqual(m, {})

    def test_6(self):
        b = Board()
        b.pointsContent = [0] * 26
        b.pointsContent[7] = -2
        b.pointsContent[12] = -5
        b.pointsContent[17] = -3
        b.pointsContent[19] = -5
        b.pointsContent[4] = 1
        b.pointsContent[3] = 3
        b.pointsContent[1] = 10
        b.pointsContent[0] = 1
        b.whiteCheckers = {7, 12, 17, 19}
        b.blackCheckers = {4, 3, 1}
        b.blackCheckersTaken = 0
        b.whiteCheckersTaken = 0

        d = Dice(4, 2)
        m = generate_moves(b, "BLACK", d)
        print(b)
        print(m)

        self.assertEqual(len(m), 2)
        # self.assertEqual(m, {"4/off 3/1", "4/2 3/off"})

    def test_7(self):
        b = Board()
        b.pointsContent = [0] * 26
        b.pointsContent[7] = -2
        b.pointsContent[12] = -5
        b.pointsContent[17] = -3
        b.pointsContent[19] = -5
        b.pointsContent[4] = 1
        b.pointsContent[3] = 3
        b.pointsContent[1] = 10
        b.pointsContent[0] = 1
        b.whiteCheckers = {7, 12, 17, 19}
        b.blackCheckers = {4, 3, 1}
        b.blackCheckersTaken = 0
        b.whiteCheckersTaken = 0

        d = Dice(2, 2)
        m = generate_moves(b, "BLACK", d)
        print(b)
        print(m)

        self.assertEqual(len(m), 2)
        # self.assertEqual(m, {"4/2 3/1 3/1 2/off", "4/2 3/1 3/1 3/1"})

    def test_8(self):
        b = Board()
        b.pointsContent = [0] * 26
        b.pointsContent[7] = -2
        b.pointsContent[12] = -5
        b.pointsContent[17] = -3
        b.pointsContent[19] = -5
        b.pointsContent[8] = 1
        b.pointsContent[3] = 3
        b.pointsContent[1] = 10
        b.pointsContent[0] = 1
        b.whiteCheckers = {7, 12, 17, 19}
        b.blackCheckers = {8, 3, 1}
        b.blackCheckersTaken = 0
        b.whiteCheckersTaken = 0

        d = Dice(2, 2)
        m = generate_moves(b, "BLACK", d)
        print(b)
        print(m)

        self.assertEqual(len(m), 4)
        # self.assertEqual(m, {"8/6 6/4 3/1 3/1", "8/6 6/4 4/2 2/off", "8/6 3/1 3/1 3/1", "8/6 6/4 4/2 3/1"})

    def test_9(self):
        b = Board()
        b.pointsContent = [0] * 26
        b.pointsContent[1] = -2
        b.pointsContent[6] = 5
        b.pointsContent[7] = 3
        b.pointsContent[8] = 4
        b.pointsContent[12] = -4
        b.pointsContent[13] = -1
        b.pointsContent[18] = 2
        b.pointsContent[19] = -3
        b.pointsContent[21] = -2
        b.pointsContent[23] = -2
        b.pointsContent[24] = -1

        b.whiteCheckers = {1, 12, 13, 19, 21, 23, 24}
        b.blackCheckers = {6, 7, 8, 18}
        b.whiteCheckersTaken = 0
        b.blackCheckersTaken = 1

        d = Dice(4, 1)
        m = generate_moves(b, "BLACK", d)
        print(b)
        print(m)

        self.assertEqual(len(m), 5)

    def test_10(self):
        b = Board()
        b.pointsContent = [0] * 26
        b.pointsContent[1] = -1
        b.pointsContent[2] = 1
        b.pointsContent[4] = 1
        b.pointsContent[5] = 2
        b.pointsContent[6] = 3
        b.pointsContent[8] = 1
        b.pointsContent[13] = 5
        b.pointsContent[21] = -13
        b.pointsContent[24] = 2
        b.whiteCheckers = {1, 21}
        b.blackCheckers = {24, 13, 8, 6, 5, 4, 2}
        b.whiteCheckersTaken = 1
        b.blackCheckersTaken = 0

        d = Dice(4, 2)
        m = generate_moves(b, "WHITE", d)
        print(b)
        print(m)

        self.assertEqual(len(m), 2)
        # self.assertEqual(m, {"bar/4 1/3", "bar/4 21/23"})

    def test_11(self):
        b = Board()
        b.pointsContent = [0] * 26
        b.pointsContent[1] = -1
        b.pointsContent[2] = 1
        b.pointsContent[4] = 1
        b.pointsContent[5] = 2
        b.pointsContent[6] = 3
        b.pointsContent[8] = 1
        b.pointsContent[13] = 5
        b.pointsContent[18] = -1
        b.pointsContent[21] = -12
        b.pointsContent[24] = 2
        b.whiteCheckers = {1, 18, 21}
        b.blackCheckers = {24, 13, 8, 6, 5, 4, 2}
        b.whiteCheckersTaken = 1
        b.blackCheckersTaken = 0

        d = Dice(4, 2)
        m = generate_moves(b, "WHITE", d)
        print(b)
        print(m)

        self.assertEqual(len(m), 4)
        # self.assertEqual(m, {"bar/4 1/3", "bar/4 21/23", "bar/2 18/20", "bar/4 18/22"})


if __name__ == '__main__':
    unittest.main()
