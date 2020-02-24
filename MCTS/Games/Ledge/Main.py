import numpy as np


class Ledge:
    def __init__(self, board_str):
        self.board_start = board_str
        self.board = np.array([int(x) for x in board_str])
        self.history = []
        self.turn = 0

    def get_state(self):
        return (str(self.history), np.array(self.board))

    def get_legal_moves(self):
        legal_moves = []
        if self.board[0] != 0:
            legal_moves.append('0')

        current_window = []
        for pos in range(self.board.size):
            if self.board[pos] == 0:
                current_window.append(pos)
                continue
            for pos_to in current_window:
                legal_moves.append("{0}_{1}".format(pos, pos_to))
            current_window = []
        return legal_moves

    def execute_move(self, move):
        if '0' == move:
            self.board[0] = 0
            self.history.append(0)
            self.turn = len(self.history) % 2
            return None

        pos_from, pos_to = map(lambda x: int(x), move.split('_'))

        assert (pos_from > pos_to >= 0)
        assert (self.board[pos_from] > 0 and self.board[pos_to] == 0)
        # TODO: check squares in between

        self.board[pos_to] = self.board[pos_from]
        self.board[pos_from] = 0
        self.history.append(move)
        self.turn = len(self.history) % 2

    def undo_move(self):
        pass

    def is_finished(self):
        return True if (self.board == 2).sum() == 0 else False

    def outcome(self):
        return [1, -1] if self.turn == 1 else [-1, 1]

    def reset(self):
        self.board = np.array([int(x) for x in self.board_start])
        self.history = []
        self.turn = 0

    def print_board(self):
        print(self.board)


if __name__ == '__main__':
    game = Ledge("110002")
    while not game.is_finished():
        game.print_board()
        print(game.get_legal_moves())
        move = input()
        game.execute_move(move)
    print(game.get_state())
    print(game.outcome())
