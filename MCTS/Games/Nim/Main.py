import numpy as np


class Nim:
    def __init__(self, pieces, max_take, starting_player=0, verbose=False):
        assert (max_take >= 1)
        assert (pieces >= 1)
        assert (pieces > max_take)

        self.pieces_start = pieces
        self.store_pieces = None
        self.board = np.array([pieces])
        self.max_take = max_take
        self.history = []
        self.store_history = None
        self.turn = starting_player
        self.store_starting_player = starting_player
        self.state_moves = {}
        self.state = ""

        if verbose:
            print("Start pile: {0} stones".format(self.pieces_start))

    @staticmethod
    def get_game_name():
        return "ledge"

    def get_turn(self):
        assert ((self.turn + self.store_starting_player) % 2 == len(self.history) % 2)
        return self.turn

    def get_state(self):
        return (self.state, np.array(self.board))

    def store_state(self):
        self.store_pieces = np.array(self.board)
        self.store_history = list(self.history)

    def load_state(self):
        self.board = np.array(self.store_pieces)
        self.history = list(self.store_history)
        if len(self.history) > 0:
            self.state = "_" + "_".join([str(x[0]) for x in self.history])
        else:
            self.state = ""

    def get_legal_moves(self):
        if self.get_state()[0] in self.state_moves:
            return self.state_moves[self.get_state()[0]]
        self.state_moves[self.get_state()[0]] = [str(x) for x in range(1, min(self.board[0] + 1, self.max_take + 1))]
        return self.state_moves[self.get_state()[0]]

    def execute_move(self, move, verbose=False):
        assert (0 < int(move) <= min(self.board[0], self.max_take))

        if verbose:
            print("Player {0} selects {1} stone{3}: Remaining stones = {2}".format(
                self.turn + 1, int(move), self.board[0] - int(move), "s" if int(move) > 1 else ""))
        self.state += "_" + str(move)
        self.board[0] -= int(move)
        self.history.append([move, np.array(self.board)])
        self.turn = (self.turn + 1) % 2

    def undo_move(self):
        self.state = "_" + "_".join(self.state.split("_")[:-1])
        self.board[0] = self.history.pop()[1]
        self.turn = (self.turn - 1) % 2

    def is_finished(self):
        return self.board[0] == 0

    def outcome(self, verbose=False):
        if verbose:
            print("Player {0} wins!\n".format((self.turn == 0) + 1))
        return [1, -1] if self.turn == 1 else [-1, 1]

    def reset(self, verbose=False):
        self.board = np.array([self.pieces_start])
        self.history = []
        self.turn = 0
        self.turn = self.store_starting_player

        if verbose:
            print("Start pile: {0} stone{1}".format(self.pieces_start, "s" if self.pieces_start > 1 else ""))

    def print_board(self):
        print(self.board[0])


if __name__ == '__main__':
    game = Nim(10, 3)
    while not game.is_finished():
        game.print_board()
        print(game.get_legal_moves())
        move = input()
        game.execute_move(move)
    print(game.get_state())
    print(game.outcome())
