import numpy as np


class Nim:
    def __init__(self, pieces, max_take, verbose=False):
        self.pieces_start = pieces
        self.store_pieces = None
        self.board = np.array([pieces])
        self.max_take = max_take
        self.history = []
        self.store_history = None
        self.turn = 0
        self.state_moves = {}
        self.state = ""

        if verbose:
            print("Start pile: {0} stones".format(self.pieces_start))

    @staticmethod
    def get_game_name():
        return "ledge"

    def get_turn(self):
        assert (self.turn == len(self.history) % 2)
        return self.turn

    def get_state(self):
        return (self.state, np.array(self.board))

    def store_state(self):
        self.store_pieces = self.board[0]
        self.store_history = list(self.history)

    def load_state(self):
        self.board[0] = self.store_pieces
        self.history = list(self.store_history)

    def get_legal_moves(self):
        if self.get_state()[0] in self.state_moves:
            return self.state_moves[self.get_state()[0]]
        self.state_moves[self.get_state()[0]] = [str(x) for x in range(1, min(self.board[0] + 1, self.max_take + 1))]
        return self.state_moves[self.get_state()[0]]

    def execute_move(self, move, verbose=False):
        assert (0 < int(move) <= min(self.board[0], self.max_take))

        if verbose:
            print("Player {0} selects {1} stones: Remaining stones = {2}".format(
                self.turn + 1, int(move), self.board[0] - int(move)))
        self.state += str(move)
        self.board[0] -= int(move)
        self.history.append([move, np.array(self.board)])
        self.turn = len(self.history) % 2

    def undo_move(self):
        self.state = self.state[:-1]
        self.board[0] = self.history.pop()[1]
        self.turn = len(self.history) % 2

    def is_finished(self):
        return self.board[0] == 0

    def outcome(self, verbose=False):
        if verbose:
            print("Player {0} wins!".format((self.turn == 0) + 1))
        return [1, -1] if self.turn == 1 else [-1, 1]

    def reset(self):
        self.board = np.array([self.pieces_start])
        self.history = []
        self.turn = 0

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
