import numpy as np
import json


class Hexagonal:
    def __init__(self, board_type, board_size, cell_types):
        self.neighbours = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]
        self.board = self._create_board(board_type, board_size, cell_types)
        self.actual_neighbours = {}

    @staticmethod
    def _create_board(board_type, dimensions, cell_types):
        '''

        @param type:
        @param dimensions:
        @param cell_types:
        @return:
        '''

        board = np.array([])
        if board_type == 'triangle':
            board = np.array([[0 if x < dimensions - y else -1 for x in range(dimensions)] for y in range(dimensions)])
        elif board_type == 'diamond':
            board = np.array([[0] * dimensions] * dimensions)
        for num, cell_type in enumerate(cell_types):
            for y, x in cell_type:
                board[y, x] = num if board[y, x] != -1 else -1
        return board

    def get_board(self):
        return self.board

    def set_board(self, board):
        self.board = board

    def get_unoccupied(self):
        return [x * self.board.shape[1] + y for x in range(self.board.shape[0]) for y in
                range(self.board.shape[1]) if self.board[x, y] == 0]

    def get_neighbours(self, pos, value):
        if pos in self.actual_neighbours:
            return self._get_matching_neighbours(self.actual_neighbours[pos], value)
        x, y = (pos // self.board.shape[1], pos % self.board.shape[1])
        neighbours = []
        num_neighbours = []
        for direction in self.neighbours:
            x_next = x + direction[0]
            y_next = y + direction[1]
            if 0 <= x_next < self.board.shape[0] and 0 <= y_next < self.board.shape[1]:
                neighbours.append([x_next, y_next])
                num_neighbours.append(x_next * self.board.shape[1] + y_next)
        self.actual_neighbours[pos] = [neighbours, num_neighbours]
        return self._get_matching_neighbours(self.actual_neighbours[pos], value)

    def _get_matching_neighbours(self, neighbours, value):
        return [neighbours[1][pos] for pos in range(len(neighbours[0])) if self.board[neighbours[0][pos][0], neighbours[0][pos][1]] == value]

    def border(self, pos):
        #
        # 0/\1
        # 2\/3
        x, y = (pos // self.board.shape[1], pos % self.board.shape[1])
        sides = []

        if x == 0:
            sides.append(1)
        if x == self.board.shape[0] - 1:
            sides.append(2)
        if y == 0:
            sides.append(0)
        if y == self.board.shape[1] - 1:
            sides.append(3)
        return sides

    def __getitem__(self, item):
        return self.board[item // self.board.shape[1], item % self.board.shape[1]]

    def __setitem__(self, key, value):
        self.board[key // self.board.shape[1], key % self.board.shape[1]] = value

    def __str__(self):
        """

        :return:
        """

        board_str = ""
        print(self.board.shape)
        for y in range(self.board.shape[0] * 2 - 1):
            board_str += " " * (abs(self.board.shape[0] - y - 1))

            for x in range(y + 1):
                if 0 <= y - x < self.board.shape[0] and x < self.board.shape[0]:
                    if self.board[y - x, x] == -1:
                        return board_str
                    board_str += str(self.board[y - x, x]) + " "
            board_str += "\n"
        return board_str


if __name__ == '__main__':
    print(Hexagonal())
