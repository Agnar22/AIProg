import numpy as np
import ast
from Board import Hexagonal


class PegSolitaire(Hexagonal.Hexagonal):

    def __init__(self):
        Hexagonal.Hexagonal.__init__(self)

    def get_state(self):
        return str(self.board)

    def get_legal_moves(self):
        """

        :return:
        """
        legal_moves = []

        for ix, iy in np.ndindex(self.board.shape):
            if self.board[ix, iy] != 1:
                continue
            for direction in self.neighbours:
                n_neighbour = (ix + direction[0], iy + direction[1])
                nn_neighbour = (ix + 2 * direction[0], iy + 2 * direction[1])
                if not (self._legal_pos(n_neighbour) and self._legal_pos(nn_neighbour)):
                    continue
                if self.board[n_neighbour] == self.board[ix, iy] == 1 and self.board[nn_neighbour] == 0:
                    legal_moves.append(str([(ix, iy), nn_neighbour]))
        # print(legal_moves)
        return legal_moves

    def _legal_pos(self, pos):
        '''

        :param pos:
        :return:
        '''
        return True if 0 <= pos[0] < self.board.shape[0] and 0 <= pos[1] < self.board.shape[0] else False

    def execute_move(self, move):
        '''

        :param move:
        :return:
        '''

        if move not in self.get_legal_moves():
            print(move, "is not a legal move!")
            return -1
        # print("executed", move)
        move = ast.literal_eval(move)

        middle = tuple(np.add(move[0], tuple(np.subtract(move[1], move[0]) // 2)))
        self.board[move[0]] = 0
        self.board[middle] = 0
        self.board[move[1]] = 1
        return self.get_state(), self.outcome() if self.is_finished() else 0

    def is_finished(self):
        return len(self.get_legal_moves()) == 0

    def outcome(self):
        """

        :return:
        """
        if np.sum(self.board == 1) == 1:
            print("Won!")
        return 1 if np.sum(self.board == 1) == 1 else -1
        # return 1 if np.sum(self.board == 1) == 1 else -np.sum(self.board == 1) / 10

    def reset(self):
        Hexagonal.Hexagonal.__init__(self)

    def print_board(self):
        to_replace = [("0", "\u25cb"), ("1", "\u2b24")]
        board_string = str(self)
        for from_chr, to_chr in to_replace:
            board_string = board_string.replace(from_chr, to_chr)
        print(board_string)

    def __getitem__(self, item):
        return self.board[item]


if __name__ == "__main__":
    PegSolitaire().print_board()
    print(PegSolitaire().get_legal_moves())
    print(PegSolitaire()[0, 3])
    game = PegSolitaire()
    game.print_board()
    print(game.execute_move([(0, 1), (0, 3)]))
