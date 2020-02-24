import numpy as np


class Nim:
    def __init__(self, pieces, max_take):
        self.pieces_start = pieces
        self.board = np.array([pieces])
        self.max_take = max_take
        self.history = []
        self.turn = 0

    def get_state(self):
        return (str(self.board), np.array(self.board))

    def get_legal_moves(self):
        return [str(x) for x in range(1, min(self.board[0] + 1, self.max_take + 1))]

    def execute_move(self, move):
        assert (0 < int(move) <= self.board[0])

        self.board[0] -= int(move)
        self.history.append(move)
        self.turn = len(self.history) % 2

    def undo_move(self):
        self.board[0] += self.history.pop()
        self.turn = len(self.history) % 2

    def is_finished(self):
        return self.board[0] == 0

    def outcome(self):
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
