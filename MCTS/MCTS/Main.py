import numpy as np
import random


# from multiprocessing import


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
        # Tree search
        state = game.get_state()
        if len(self.states[state][1]) > 0:
            move = self._tree_search(game)
            game.execute_move(move)
            outcome = self._single_search(game)
            game.undo_move()

        # Node expansion
        moves = game.get_moves()
        self.states[state][1] = moves
        for action in moves:
            self.state_action[state + '_' + action] = [0, 0]

        # Leaf evaluation
        evaluation = self.rollout(game)

        # Backpropagation
        return evaluation

    def _tree_search(self, game):
        pass

    def _node_expansion(self):
        pass

    def rollout(self, game):
        while not game.is_finished():
            moves = game.get_moves()
            game.execute_move(moves[random.randint(len(moves))])
        return game.outcome()

    def backpropagation(self):
        pass

    @staticmethod
    def uct():
        pass

    def reset(self):
        self.states = {}
        self.state_action = {}
