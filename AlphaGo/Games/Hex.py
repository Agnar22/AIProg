import numpy as np
from Games.Hexagonal import Hexagonal


class Hex:

    def __init__(self, board_size, cell_types, starting_player):
        self.hex_board = Hexagonal("diamond", board_size, cell_types)
        self.store_board = np.array([])
        self.history = []
        self.store_history = []
        self.state = ""
        self.starting_player = starting_player

    def get_state(self):
        return (self.state, np.array(self.hex_board.get_board()))

    def get_turn(self):
        return (len(self.history) + self.starting_player + 1) % 2 + 1

    def store_state(self):
        self.store_board = np.array(self.hex_board.get_board())
        self.store_history = list(self.history)

    def load_state(self):
        self.hex_board.set_board(np.array(self.store_board))
        self.history = list(self.store_history)

    def get_legal_moves(self):
        return self.hex_board.get_unoccupied()

    def _legal_pos(self, pos):
        pass

    def execute_move(self, move):
        #assert (self.hex_board[int(move)] == 0)
        self.state += "_" + str(move)
        self.history.append((int(move), np.array(self.hex_board.get_board())))
        self.hex_board[int(move)] = self.get_turn()

    def undo_move(self):
        move, board = self.history.pop()
        self.hex_board.set_board(board)
        self.state = self.state[:-len(str(move)) - 1]

    def is_finished(self):
        # This assumes that we did not start in a finished position
        if len(self.history) == 0:
            return False
        border = [False, False, False, False]

        neighbours = [self.history[-1][0]]
        pos = 0
        added_neighbours = {self.history[-1][0]}
        colour = self.hex_board[self.history[-1][0]]

        while pos < len(neighbours):
            curr_pos = neighbours[pos]
            border_sides = self.hex_board.border(curr_pos)
            for x in border_sides:
                border[x] = True

            curr_neighbours = self.hex_board.get_neighbours(curr_pos, colour)
            for neighbour in curr_neighbours:
                if neighbour not in added_neighbours:
                    neighbours.append(neighbour)
                    added_neighbours.add(neighbour)
            pos += 1

        # TODO: not correct if player 1 is not starting??? (question of definition)
        return True if (border[0] and border[3] and colour == 1) or \
                       (border[1] and border[2] and colour == 2) else False

    def outcome(self):
        # Assuming that the game is finished
        return (len(self.history) + self.starting_player) % 2

    def reset(self):
        pass

    def print_board(self):
        print(str(self.hex_board))


visited = set()
branching_sum = [0]
depth_sum = [0]

end_pos = [0]


def dfs(game):
    if game.is_finished():
        depth_sum[0] += len(game.history)
        # game.print_board()
        return 1 if game.outcome() == 1 else 0, 1
    if game.get_state()[0] in visited:
        return 0, 0
    else:
        # game.print_board()
        visited.add(game.get_state()[0])

    if len(game.history) == 4:
        end_pos[0] += 1
        return 0, 1

    num_solved = 0
    num_visited = 0
    leg_moves = game.get_legal_moves()
    branching_sum[0] += len(leg_moves)
    # print(len(leg_moves))
    # print("moves: ", leg_moves)
    for move in leg_moves:
        game.execute_move(move)
        temp_solved, temp_visited = dfs(game)
        game.undo_move()
        num_solved += temp_solved
        num_visited += temp_visited
    return num_solved, num_visited


if __name__ == "__main__":
    # TODO: handle overlapping positions???
    # DFS of game
    import time

    now = time.time()
    game = Hex(5, [], 1)
    print("num_solved, num_visied", dfs(game))
    print("time", time.time() - now)
    print("branching_sum", branching_sum)
    print("depth_sum", depth_sum)
    print("num_pos", len(visited))
    print(end_pos)
