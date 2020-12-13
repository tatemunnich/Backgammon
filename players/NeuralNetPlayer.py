import json
import tensorflow as tf
from board.Board import getPieceSymbol, BLACK, Board, WHITE, getOtherColor
from move.MovementFactory import generate_moves
from players.Player import Player


class NeuralNetPlayer(Player):
    def __init__(self, color, network, name="Net", learning=False):
        self.name = name
        self.network = network
        self.color = color
        self.learning = learning

    # def get_move(self, backgammon, return_value=False):
    #     moves = generate_moves(backgammon.board, BLACK, backgammon.dice)
    #     best, value = None, 0
    #     for move in moves:
    #         new_value = self.network.calculate
    #         if new_value > value:
    #             best = move
    #             value = new_value
    #     if return_value:
    #         return best, value
    #     else:
    #         return best

    def get_move(self, backgammon):
        # pa4 specs
        to_move = self.color
        next_player = getOtherColor(self.color)

        board = backgammon.board
        moves = generate_moves(board, to_move, backgammon.dice)
        best, value, output = None, -1000000, None
        for move in moves:
            new_value, new_output = self.evaluate(move.board_after, next_player, to_move)
            # print(move, " with value", new_value)
            if new_value > value:
                best = move
                value = new_value
                output = new_output

        if self.learning:
            self.evaluate(board, to_move, to_move)
            self.network.backprop(output)

        return best

    def lost(self, board, value):
        if self.learning:
            if self.network.num_outputs == 1:
                if self.color == BLACK:
                    expected = tf.constant([[0.]])
                elif self.color == WHITE:
                    expected = tf.constant([[1.]])
            elif self.network.num_outputs == 4:
                if self.color == BLACK:
                    if value == 1:
                        expected = tf.constant([[0., 0., 1., 0.]])
                    else:
                        expected = tf.constant([[0., 0., 0., 1.]])
                elif self.color == WHITE:
                    if value == 1:
                        expected = tf.constant([[1., 0., 0., 0.]])
                    else:
                        expected = tf.constant([[0., 1., 0., 0.]])

            self.evaluate(board, self.color, self.color)
            self.network.backprop(expected)

    def won(self, board, value):
        if self.learning:
            if self.network.num_outputs == 1:
                if self.color == BLACK:
                    expected = tf.constant([[1.]])
                elif self.color == WHITE:
                    expected = tf.constant([[0.]])
            elif self.network.num_outputs == 4:
                if self.color == WHITE:
                    if value == 1:
                        expected = tf.constant([[0., 0., 1., 0.]])
                    else:
                        expected = tf.constant([[0., 0., 0., 1.]])
                elif self.color == BLACK:
                    if value == 1:
                        expected = tf.constant([[1., 0., 0., 0.]])
                    else:
                        expected = tf.constant([[0., 1., 0., 0.]])

            self.evaluate(board, getOtherColor(self.color), self.color)
            self.network.backprop(expected)

    def __str__(self):
        return self.name + " (" + getPieceSymbol(self.color) + ")"

    @staticmethod
    def get_input_vector(board=Board(), current_color=BLACK):
        """
             BLACK_OFF | BLACK_POINTS_CONTENT | BLACK_BAR | TURN | WHITE_BAR | WHITE_POINTS CONTENT | WHITE_OFF
                 1            24 * 4 = 96          1         2         1           24 * 4 = 96            1
        """
        black = []
        white = []
        for point, v in enumerate(board.pointsContent[1:-1], 1):
            if v > 0:
                white.extend((0, 0, 0, 0))
                if v == 1:
                    black.extend((1, 0, 0, 0))
                elif v == 2:
                    black.extend((1, 1, 0, 0))
                elif v == 3:
                    black.extend((1, 1, 1, 0))
                else:
                    black.extend((1, 1, 1, (v - 3) / 2))

            elif v < 0:
                black.extend((0, 0, 0, 0))
                if v == -1:
                    white.extend((1, 0, 0, 0))
                elif v == -2:
                    white.extend((1, 1, 0, 0))
                elif v == -3:
                    white.extend((1, 1, 1, 0))
                else:
                    white.extend((1, 1, 1, (abs(v) - 3) / 2))
            else:
                black.extend((0, 0, 0, 0))
                white.extend((0, 0, 0, 0))
        current_color = [1, 0] if current_color == BLACK else [0, 1]
        middle = black + [board.numBar(BLACK) / 2] + current_color + [board.numBar(WHITE) / 2] + white
        return tf.constant([[board.numOff(BLACK) / 15] + middle + [board.numOff(WHITE) / 15]])

    def evaluate(self, board, color_to_move, color):
        x = self.get_input_vector(board, color_to_move)
        outputs = self.network.calculate(x)
        if self.network.num_outputs == 1:
            if color == BLACK:
                return outputs[0][0], outputs
            elif color == WHITE:
                return 1 - outputs[0][0], outputs
        elif self.network.num_outputs == 4:  # black win, black gammon, white win, white gammon
            if color == BLACK:
                return outputs[0][0] + 2*outputs[0][1] - outputs[0][2] - 2*outputs[0][3], outputs
            elif color == WHITE:
                return -outputs[0][0] - 2*outputs[0][1] + outputs[0][2] + 2*outputs[0][3], outputs
        else:
            raise Exception("Could not evaluate output shape")


class NeuralNet:
    def __init__(self, checkpoint_dir, num_inputs=198, num_hidden=40, num_outputs=1,
                 hidden_weights=False, second_weights=None, save_traces=False):
        self.inputs = None  # shape (1, num_inputs)
        self.hidden_outputs = None  # shape (1, num_hidden)
        self.outputs = None  # shape (1, num_outputs)

        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs

        if hidden_weights:
            self.hidden_weights = tf.Variable(tf.identity(hidden_weights))  # shape (num_inputs, num_hidden)
            self.second_weights = tf.Variable(tf.identity(second_weights))  # shape (num_hidden, num_outputs)
            print('hi')
        else:
            self.randomize_weights()

        self.checkpoint_dir = checkpoint_dir
        self.ckpt = self.make_checkpoint()

        self.save_traces = save_traces
        self.ew = tf.Variable(tf.zeros(shape=(num_hidden, num_outputs)))  # shape (num_hidden, num_outputs)
        self.ev = tf.Variable(tf.zeros(shape=(num_inputs, num_hidden, num_outputs)))  # shape (num_inputs, num_hidden, num_outputs)

    def randomize_weights(self):
        self.hidden_weights = tf.Variable(tf.random.uniform(minval=-1., maxval=1.,
                                                            shape=(self.num_inputs, self.num_hidden)))
        self.second_weights = tf.Variable(tf.random.uniform(minval=-1., maxval=1.,
                                                            shape=(self.num_hidden, self.num_outputs)))

    def calculate(self, inputs):
        activator = tf.sigmoid
        self.inputs = inputs
        self.hidden_outputs = activator(tf.matmul(inputs, self.hidden_weights))
        self.outputs = activator(tf.tensordot(self.hidden_outputs, self.second_weights, axes=1))
        return self.outputs

    def make_checkpoint(self):
        try:
            if self.save_traces:
                return tf.train.Checkpoint(hidden_weights=self.hidden_weights, second_weights=self.second_weights,
                                           ew=self.ew, ev=self.ev)
            else:
                return tf.train.Checkpoint(hidden_weights=self.hidden_weights, second_weights=self.second_weights)
        except AttributeError:  # for checkpoints without save traces attribute
            return tf.train.Checkpoint(hidden_weights=self.hidden_weights, second_weights=self.second_weights)

    def save(self):
        self.ckpt.save(self.checkpoint_dir + "/ckpt")

    def save_to_text(self, filename):
        with open('./checkpoints/' + str(self.num_outputs) + ' text_new/' + filename, 'w') as f:
            weights = {"hidden": self.hidden_weights.numpy().tolist(), "second": self.second_weights.numpy().tolist(),
                       "ew": self.ew.numpy().tolist(), "ev": self.ev.numpy().tolist()}
            json.dump(weights, f)

    def load(self, num=None, text_path=False):
        if text_path:
            with open(text_path) as f:
                o = json.load(f)

            ohw = tf.Variable(o['hidden'])
            osw = tf.Variable(o['second'])
            oew = tf.Variable(o['ew'])
            oev = tf.Variable(o['ev'])

            self.second_weights = osw
            self.hidden_weights = ohw
            self.ew = oew
            self.ev = oev
            return
        if num is None:
            status = self.ckpt.restore(tf.train.latest_checkpoint(self.checkpoint_dir))
        else:
            status = self.ckpt.restore(self.checkpoint_dir + "/ckpt-" + str(num))
        status.assert_consumed()
        self.inputs = None
        self.hidden_outputs = None
        self.outputs = None

    @staticmethod
    def gradient(unit):
        return tf.math.multiply(unit, (tf.ones_like(unit) - unit))

    def backprop(self, expected):
        # As specified in gettysburg PA4
        lambd = 0.7
        alpha = 0.1
        beta = 0.1
        self.ew = lambd * self.ew + tf.tensordot(self.hidden_outputs, NeuralNet.gradient(self.outputs), axes=[0, 0])
        self.ev = lambd * self.ev + \
                  tf.tensordot(self.inputs[0],
                               tf.math.multiply(tf.tensordot(NeuralNet.gradient(self.hidden_outputs),
                                                             NeuralNet.gradient(self.outputs), axes=[0, 0]),
                                                self.second_weights), axes=0)

        error = expected - self.outputs

        second_weights_change = beta * (self.ew * error)  # scalar, (num_hidden, num_outputs), (1, num_outputs)
        self.second_weights.assign_add(second_weights_change)

        hidden_weights_change = alpha * tf.tensordot(self.ev, error[0], axes=1)
        self.hidden_weights.assign_add(hidden_weights_change)

