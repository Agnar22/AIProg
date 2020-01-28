import numpy as np
import json


class Hexagonal:
    def __init__(self):
        # self.neighbours = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 1)]
        self.neighbours = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]
        self.data = {}
        with open('PivotalParameters.json') as json_file:
            self.data = json.load(json_file)
        self.board = self._create_board(self.data['board_type'], self.data['board_size'], self.data['cell_types'])

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
            # board = np.array([[0 if x <= y else -1 for x in range(dimensions)] for y in range(dimensions)])
            board = np.array([[1 if x < dimensions - y else -1 for x in range(dimensions)] for y in range(dimensions)])
        elif board_type == 'diamond':
            # board = np.array(
            #     [[0 if (x <= y and y < dimensions) or (x <= 2 * dimensions - y - 2 and y >= dimensions) else -1 for x in
            #       range(dimensions)] for y in range(2 * dimensions - 1)])
            board = np.array([[1] * dimensions] * dimensions)
        for num, cell_type in enumerate(cell_types):
            for y, x in cell_type:
                board[y, x] = num if board[y, x] != -1 else -1
        return board

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
