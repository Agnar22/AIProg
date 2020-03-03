import numpy as np


class Ledge:

    def __init__(self, board_str, starting_player=0, verbose=False):
        assert (1 == board_str.count("2"))
        assert (len(set(board_str).difference({"0", "1", "2"})) == 0)

        self.board_start = board_str
        self.board = np.array([int(x) for x in board_str])
        self.store_board = None
        self.history = []
        self.store_history = None
        self.turn = starting_player
        self.store_starting_player = starting_player
        self.state_moves = {}
        self.state = ""

        if verbose:
            print("Start board: {0}".format(str(self.board)))

    @staticmethod
    def get_game_name():
        return "ledge"

    def store_state(self):
        self.store_board = np.array(self.board)
        self.store_history = list(self.history)

    def load_state(self):
        self.board = np.array(self.store_board)
        self.history = list(self.store_history)

    def get_turn(self):
        assert ((self.turn + self.store_starting_player) % 2 == len(self.history) % 2)
        return self.turn

    def get_state(self):
        return (self.state, np.array(self.board))

    def get_legal_moves(self):
        # if self.get_state()[0] in self.state_moves:
        #     return self.state_moves[self.get_state()[0]]

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
        # self.state_moves[self.get_state()[0]] = legal_moves.copy()
        return legal_moves

    def execute_move(self, move, verbose=False):
        if '0' == move:
            material = 'copper' if self.board[0] == 1 else 'gold'
            self.state += '_0'
            self.board[0] = 0
            if verbose:
                print('Player {0} picks up {1}: {2}'.format(self.turn + 1, material, str(self.board)))
            self.history.append([0, np.array(self.board)])
            self.turn = (self.turn + 1) % 2
            return None

        pos_from, pos_to = map(lambda x: int(x), move.split('_'))

        assert (pos_from > pos_to >= 0)
        assert (self.board[pos_from] > 0 and self.board[pos_to] == 0)
        # TODO: check squares in between

        self.state += '_' + str(pos_from) + str(pos_to)
        self.board[pos_to] = self.board[pos_from]
        self.board[pos_from] = 0

        if verbose:
            material = 'copper' if self.board[pos_to] == 1 else 'gold'
            print('Player {0} moves {1} from cell {2} to {3}: {4}'.format(self.turn + 1, material, pos_from, pos_to,
                                                                          str(self.board)))
        self.history.append([move, np.array(self.board)])
        self.turn = (self.turn + 1) % 2

    def undo_move(self):
        self.state = '_'.join(self.state.split('_')[:-1])
        self.board = np.array(self.history.pop()[1])
        self.turn = (self.turn - 1) % 2

    def is_finished(self):
        return True if (self.board == 2).sum() == 0 else False

    def outcome(self, verbose=False):
        if verbose:
            print("Player {0} wins!\n".format((self.turn == 0) + 1))
        return [1, -1] if self.turn == 1 else [-1, 1]

    def reset(self, verbose=False):
        self.board = np.array([int(x) for x in self.board_start])
        self.history = []
        self.turn = self.store_starting_player

        if verbose:
            print("Start board: {0}".format(str(self.board)))

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
