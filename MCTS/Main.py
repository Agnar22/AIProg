from Games.Nim import Main as Nim
from Games.Ledge import Main as Ledge
from MCTS import Main as MCTS
from multiprocessing import Pool
import json
import time
import random


def read_json(filepath):
    with open(filepath) as f:
        return json.load(f)


class GameSimulator:
    def __init__(self, tree_class, game_class, game_params):
        self.tree_class = tree_class
        self.game_class = game_class
        self.game_params = game_params

    def run(self, processes, batch_size, player_starting, verbose, searches, exp_param):
        player_starting -= 1

        players_starting = [player_starting if player_starting != 2 else random.randint(0, 1) for _ in range(batch_size)]
        print(f"Player 1 starting {len(list(filter(lambda x:x==0, players_starting)))} out of {batch_size} matches.")
        trees = [self.tree_class() for _ in range(batch_size)]
        games = [self.game_class(*self.game_params, starting_player=players_starting[x]) for x in range(batch_size)]
        verboses = [verbose for _ in range(batch_size)]
        players_starting = [player_starting for _ in range(batch_size)]
        searches = [searches for _ in range(batch_size)]
        exp_params = [exp_param for _ in range(batch_size)]

        now = time.time()
        p = Pool(processes)
        results = p.map(GameSimulator.simulate_game,
                        zip(trees, games, verboses, players_starting, searches, exp_params))
        p.close()
        p.join()
        print(f"Time: {time.time() - now}")

        num_won = len(list(filter(lambda x: x[0] > 0, results)))
        print("Player 1 won {0} out of {1} matches ({2:.1f} %)".format(num_won, batch_size, 100 * num_won / batch_size))

    @staticmethod
    def simulate_game(args):
        tree, game, verbose, player_starting, searches, exp_param = args
        game.reset(verbose=verbose)
        tree.set_exp_param(exp_param)

        while not game.is_finished():
            state = game.get_state()[0]
            tree.search(game, searches)
            # print(tree.get_search_statistics(state))
            # print("move", mcts.get_recommended_move(state))
            game.execute_move(tree.get_recommended_move(state), verbose=verbose)
            tree.reset()
        return game.outcome(verbose=verbose)


if __name__ == '__main__':
    params = read_json("PivotalParameters.json")
    if params['games']['playing'] == 'nim':
        game = Nim.Nim
        sim = GameSimulator(MCTS.MCTS, game, [params["games"]["nim"]["startPieces"], params["games"]["nim"]["maxTake"]])
    else:
        game = Ledge.Ledge
        sim = GameSimulator(MCTS.MCTS, game, [params["games"]["ledge"]["startPieces"]])
    sim.run(*params['simulator'].values())
