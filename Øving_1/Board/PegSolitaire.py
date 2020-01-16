import numpy as np
import Hexagonal


class PegSolitaire(Hexagonal.Hexagonal):

    def __init__(self):
        Hexagonal.Hexagonal.__init__(self)

    def get_legal_moves(self):
        """

        :return:
        """
        legal_moves = []

        for ix, iy in np.ndindex(self.board.shape):
            for direction in self.neghbours:
                n_neighbour = (ix + direction[0], iy + direction[1])
                nn_neighbour = (ix + 2 * direction[0], iy + 2 * direction[1])
                if not (self._legal_pos(n_neighbour) and self._legal_pos(nn_neighbour)):
                    break
                if
            print(self.board[ix, iy])

    def _legal_pos(self, pos):
        return True if 0 <= pos[0] < self.board.shape[0] and 0 <= pos[1] < self.board.shape[0] else False

    def execute_move(self, move):
        """:arg"""
        pass

    def outcome(self):
        """

        :return:
        """
        pass

    def print_board(self):
        to_replace = [("0", "\u2B58"), ("1", "\u2b24")]
        board_string = str(self)
        for from_chr, to_chr in to_replace:
            board_string = board_string.replace(from_chr, to_chr)
        print(board_string)


if __name__ == "__main__":
    PegSolitaire().print_board()
    PegSolitaire().get_legal_moves()
