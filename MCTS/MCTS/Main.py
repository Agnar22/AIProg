import numpy as np
import random
import math


class MCTS:
    def __init__(self):
        self.states = {}  # visits, [actions]
        self.state_action = {}  # visits, sum q values

    def search(self, game, search_num):
        game.store_state()
        self.states[game.get_state()] = [0, []]
        for _ in range(search_num):
            self._single_search(game)
            game.load_state()

    def _single_search(self, game):
        if game.is_final(): return game.outcome

        # Tree search
        state = game.get_state()[0]
        if len(self.states[state][1]) > 0:
            outcome = self._tree_search(game, state)
            return outcome

        # Node expansion
        self._node_expansion(game, state)

        # Leaf evaluation
        evaluation = self.rollout(game)

        # Backpropagation
        return evaluation

    def _tree_search(self, game, state):
        move = self._select_move(game, state)
        game.execute_move(move)
        outcome = self._single_search(game)
        game.undo_move()

        self.states[state][0] = self.states[state][0] + 1
        move_statistics = self.state_action[state + '_' + move]
        move_statistics[0] += 1
        move_statistics[1] += outcome[game.get_turn()]
        self.state_action[state + '_' + move] = move_statistics
        return outcome

    def _select_move(self, game, state):
        max_val = None
        max_action = None

        for action in game.get_moves():
            score = MCTS.uct(1, self.state[state], self.state_action[state + '_' + action])
            if score == None: return action
            if score > max_val:
                max_val = score
                max_action = action
        return max_action

    def _node_expansion(self, game, state):
        moves = game.get_moves()
        self.states[state][1] = moves
        for action in moves:
            self.state_action[state + '_' + action] = [0, 0]

    def rollout(self, game):
        move_count = 0
        while not game.is_finished():
            moves = game.get_moves()
            game.execute_move(moves[random.randint(len(moves))])
            move_count += 1

        for _ in range(move_count):
            game.undo_move()
        return game.outcome()

    def backpropagation(self):
        pass

    @staticmethod
    def uct(c, parent, child):
        if child[0] == 0: return None

        exploration = c * math.sqrt(math.log(parent[0]) / child[0])
        q_value = child[1] / child[0]
        return q_value + exploration

    def reset(self):
        self.states = {}
        self.state_action = {}


if __name__ == '__main__':
    pass

