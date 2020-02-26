from Games.Nim import Main as Nim
from Games.Ledge import Main as Ledge
from MCTS import Main as MCTS
from multiprocessing import Pool
import json


def simulate_game(args):
    tree, game = args

    while not game.is_finished():
        state = game.get_state()[0]
        tree.search(game, 5000)
        # print(mcts.get_search_statistics(state))
        # print("move", mcts.get_recommended_move(state))
        game.execute_move(tree.get_recommended_move(state), verbose=False)
        tree.reset()
    # print(game.outcome(verbose=True))
    return game.outcome(verbose=False)


def read_json(filepath):
    with open(filepath) as f:
        return json.load(f)


class GameSimulator:
    def __init__(self, tree_class, game_class, game_params):
        self.tree_class = tree_class
        self.game_class = game_class
        self.game_params = game_params

    def run(self, batch_size):
        trees = [self.tree_class() for _ in range(batch_size)]
        games = [self.game_class(*self.game_params) for _ in range(batch_size)]
        p = Pool(8)
        results = p.map(simulate_game, zip(trees, games))
        p.close()
        p.join()
        num_won = len(list(filter(lambda x: x[0] > 0, results)))
        print("Player 1 won {0} out of {1} matches ({2:.1f} %)".format(num_won, batch_size, 100 * num_won / batch_size))


if __name__ == '__main__':
    params = read_json("PivotalParameters.json")
    # game = Ledge.Ledge
    # sim = GameSimulator(MCTS.MCTS, game, [params["games"]["ledge"]["startPieces"]])
    game = Nim.Nim
    sim = GameSimulator(MCTS.MCTS, game, [params["games"]["nim"]["startPieces"], params["games"]["nim"]["maxTake"]])

    sim.run(params['simulator']['batchSize'])

    # TODO: is store state and load state working correctly?
    # TODO: set starting player (and random)
    # game = Nim.Nim(16, 3, verbose=True)
    # game = Ledge.Ledge("000012", verbose=True)
    # mcts = MCTS.MCTS()
    #
    # while not game.is_finished():
    #     state = game.get_state()[0]
    #     mcts.search(game, 4000)
    #     # print(mcts.get_search_statistics(state))
    #     # print("move", mcts.get_recommended_move(state))
    #     game.execute_move(mcts.get_recommended_move(state), verbose=True)
    #     mcts.reset()
    # print(game.outcome(verbose=True))
