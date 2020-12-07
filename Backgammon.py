import cProfile
import random

from board.Board import Board, BLACK, WHITE, NONE
from board.Dice import Dice

from players.Player import RandomPlayer, MinimaxPlayer, HumanPlayer, GnuPlayer, AlphaBeta


class Backgammon:

    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.board = Board()
        self.dice = Dice()
        self.on_roll = 0  # starting player 1

    def reset(self):
        self.board = Board()
        self.on_roll = 0

    def do_move(self, move):
        self.board.applyBoard(move.board_after)
        self.dice.roll()
        self.on_roll = (self.on_roll + 1) % 2

    def start_game(self, verbose=False):
        player1_roll, player2_roll = 0, 0
        while player1_roll == player2_roll:
            player1_roll = random.randint(1, 6)
            player2_roll = random.randint(1, 6)
            if verbose:
                print(self.players[0], "rolls", str(player1_roll) + ",", self.players[1], "rolls", str(player2_roll) + ".")
        self.on_roll = 0 if player1_roll > player2_roll else 1
        self.dice.setRoll((player1_roll, player2_roll))

    def run(self, verbose=False):
        self.start_game(verbose=verbose)
        if verbose:
            print(self.board)
            print(str(self.players[self.on_roll]) + " goes first.")
        while True:
            if verbose:
                print("")
                print(str(self.players[self.on_roll]) + " rolled " + str(self.dice))
            move = self.players[self.on_roll].get_move(self)
            self.do_move(move)
            if verbose:
                print(self.board)
                print(move)
            if self.board.getWinner() != NONE:
                if verbose:
                    print("Winner, " + self.board.getWinner())
                return self.board.getWinner(game_value=True)
            ##################################################
            if verbose:
                print("")
                print(str(self.players[self.on_roll]) + " rolled " + str(self.dice))
            move = self.players[self.on_roll].get_move(self)
            self.do_move(move)
            self.board.applyBoard(move.board_after)
            if verbose:
                print(self.board)
                print(move)
            if self.board.getWinner() != NONE:
                if verbose:
                    print("Winner, " + self.board.getWinner())
                return self.board.getWinner(game_value=True)

    @staticmethod
    def benchmark(player1, player2, num_games):
        scores = {BLACK: 0, WHITE: 0}
        back = Backgammon(player1(BLACK), player2(WHITE))
        for i in range(num_games):
            winner, value = back.run(verbose=True)
            print("Game", str(i+1) + ":", winner, "wins a", value, "game")
            scores[winner] += value
            back.reset()
        print(scores)
        return scores


def runRandomTime():
    b = Backgammon(RandomPlayer(BLACK), GnuPlayer(WHITE))
    for i in range(3):
        print(b.run(verbose=True))
        b.reset()


if __name__ == "__main__":
    b = Backgammon(RandomPlayer(BLACK), GnuPlayer(WHITE))
    # cProfile.run('runRandomTime()')
    # # s = "0;1;0;1;1;Crazy Carl;gnubg;0;0;0;1;1;0;8;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;-2;0;0;0;"
    b.benchmark(RandomPlayer, GnuPlayer, 100)
