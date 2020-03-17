import numpy as np
import random
import math


class MCTS:
    def __init__(self):
        self.states = {}  # visits, [actions]
        self.state_action = {}  # [visits, sum q values]

    def get_recommended_move(self, state):
        max_visits = None
        best_action = None
        for action in self.states[state][1]:
            visits = self.state_action[state + '_' + action][0]
            if max_visits == None or visits > max_visits:
                max_visits = visits
                best_action = action
        return best_action

    def get_search_statistics(self, state):
        return self.states[state], [self.state_action[state + '_' + action] for action in self.states[state][1]]

    def set_exp_param(self, exp_param):
        self.exp_param = exp_param

    def search(self, game, search_num):
        game.store_state()
        for _ in range(search_num):
            self._single_search(game)
            game.load_state()

    def _single_search(self, game):
        if game.is_finished():
            return game.outcome()

        state = game.get_state()[0]

        # Tree search
        if state in self.states:
            outcome = self._tree_search(game, state)
            return outcome

        # Node expansion
        self._node_expansion(game, state)

        # Leaf evaluation
        action, evaluation = self.rollout(game)

        # Backpropagation
        self.states[state][0] = self.states[state][0] + 1
        self.state_action[state + '_' + action] = [1, evaluation[game.get_turn()]]
        return evaluation

    def _tree_search(self, game, state):
        # _select_move employs the tree policy (uct) when choosing action
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

        for action in game.get_legal_moves():
            print(state)
            score = MCTS.uct(self.exp_param, self.states[state], self.state_action[state + '_' + action])
            if score == None: return action
            if max_val == None or score > max_val:
                max_val = score
                max_action = action
        return max_action

    def _node_expansion(self, game, state):
        self.states[state] = [0, []]
        moves = game.get_legal_moves()
        self.states[state][1] = moves
        for action in moves:
            self.state_action[state + '_' + action] = [0, 0]

    def rollout(self, game):
        # A random behaviour policy
        first_action = None
        move_count = 0
        while not game.is_finished():
            moves = game.get_legal_moves()
            rand = random.randint(0, len(moves) - 1)
            if move_count == 0: first_action = moves[rand]
            game.execute_move(moves[rand])
            move_count += 1

        for _ in range(move_count):
            game.undo_move()
        return first_action, game.outcome()

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
