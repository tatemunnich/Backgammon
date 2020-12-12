import random

from board.Board import Board, BLACK, WHITE, NONE
from board.Dice import Dice
from players.GnuPlayer import GnuPlayer
from players.MinimaxPlayer import AlphaBetaPlayer, MinimaxPlayer
from players.NeuralNetPlayer import NeuralNetPlayer, NeuralNet
from players.RandomPlayer import RandomPlayer
from players.TatePlayer import TatePlayer
from players.heuristics import PipRatio


class Backgammon:

    def __init__(self, player1, player2):
        if not {player1.color, player2.color} == {WHITE, BLACK}:
            raise Exception("Must have one player of each color")
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

    def get_current_player(self):
        return self.players[self.on_roll]

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
            winner, value = self.board.getWinner(game_value=True)
            if winner != NONE:
                if self.players[0].color == winner:
                    self.players[0].won(self.board, value)
                    self.players[1].lost(self.board, value)
                else:
                    self.players[0].lost(self.board, value)
                    self.players[1].won(self.board, value)
                if verbose:
                    print("Winner, " + winner)
                return winner, value
            ##################################################
            if verbose:
                print("")
                print(str(self.players[self.on_roll]) + " rolled " + str(self.dice))
            move = self.players[self.on_roll].get_move(self)
            self.do_move(move)
            if verbose:
                print(self.board)
                print(move)
            winner, value = self.board.getWinner(game_value=True)
            if winner != NONE:
                if self.players[0].color == winner:
                    self.players[0].won(self.board, value)
                    self.players[1].lost(self.board, value)
                else:
                    self.players[0].lost(self.board, value)
                    self.players[1].won(self.board, value)
                if verbose:
                    print("Winner, " + winner)
                return winner, value

    @staticmethod
    def train(network, iters, start_trial=0, verbose=False):
        p1, p2 = NeuralNetPlayer(BLACK, network, learning=True), NeuralNetPlayer(WHITE, network, learning=True)
        backgammon = Backgammon(p1, p2)
        for i in range(1, iters+1):
            winner, _ = backgammon.run()
            backgammon.reset()
            print("\rGame", i+start_trial, "finished", end="")
            if i % 1000 == 0 and i != 0:
                latest_net = p1.network if winner == BLACK else p2.network
                latest_net.save()
                latest_net.save_to_text(str(i+start_trial)+".txt")
                p1.learning = False
                print("After", i + start_trial, "rounds of training:")
                Backgammon.benchmark(p1, TatePlayer(WHITE), 15)
                p1.learning = True

    @staticmethod
    def benchmark(player1, player2, num_games):
        scores = {BLACK: 0, WHITE: 0}
        wins = {BLACK: 0, WHITE: 0}
        back = Backgammon(player1, player2)
        for i in range(num_games):
            winner, value = back.run(verbose=False)
            print("\rGame", str(i+1) + ":", winner, "wins a", value, "game", end="")
            scores[winner] += value
            wins[winner] += 1
            back.reset()
        print(scores)
        print(wins)
        return scores


def runRandomTime():
    b = Backgammon(RandomPlayer(BLACK), GnuPlayer(WHITE))
    for i in range(3):
        print(b.run(verbose=True))
        b.reset()


if __name__ == "__main__":
    # cProfile.run('runRandomTime()')
    # # s = "0;1;0;1;1;Crazy Carl;gnubg;0;0;0;1;1;0;8;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;-2;0;0;0;"
    net = NeuralNet(num_outputs=4)
    net.load()
    print(net.hidden_weights)
    Backgammon.train(net, 15000, start_trial=15000)
