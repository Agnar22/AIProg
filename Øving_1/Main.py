import json

from matplotlib import pyplot as plt
from Board import PegSolitaire, Visualize
from ActorCritic import Main as ActorCritic
from ActorCritic import Actor, Critic, CriticModules

visited = set()
branching_sum = [0]
depth_sum = [0]


def dfs(game):
    if game.is_finished():
        depth_sum[0] += len(game.history)
        # game.print_board()
        return 1 if game.outcome() == 1 else 0, 1
    if game.get_state()[0] in visited:
        return 0, 0
    else:
        visited.add(game.get_state()[0])

    num_solved = 0
    num_visited = 0
    leg_moves = game.get_legal_moves()
    branching_sum[0] += len(leg_moves)
    if len(leg_moves) > 10:
        print(len(leg_moves))
        print(leg_moves)
        game.print_board()
    for move in leg_moves:
        game.execute_move(move)
        temp_solved, temp_visited = dfs(game)
        game.undo_move()
        num_solved += temp_solved
        num_visited += temp_visited
    return num_solved, num_visited


def read_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def setup_game(param, game_class):
    return game_class(param['board_type'], param['board_size'], param['cell_types'])


def setup_actor_critic(param, game, ac_class, actor_class, critic_class, critic_table, critic_nn):
    actor = actor_class(param['lr_actor'])

    critic_module = critic_table(param['lr_critic']) if param['critic_mode'] == 'table' \
        else critic_nn(param['lr_critic'], param['network_structure'])
    critic = critic_class(critic_module)

    return ac_class(game, actor, critic)


if __name__ == '__main__':
    # # DFS of game
    # game = PegSolitaire.PegSolitaire()
    # game.print_board()
    # print(dfs(game))
    # print(branching_sum)
    # print(depth_sum)
    # print(len(visited))

    # Training ac to master Peg solitaire
    param = read_json("PivotalParameters.json")
    game = setup_game(param, PegSolitaire.PegSolitaire)
    ac = setup_actor_critic(param, game, ActorCritic.ActorCritic, Actor.Actor,
                            Critic.Critic, CriticModules.Table, CriticModules.NNApproximator)

    # for _ in range(1):
    #     game = PegSolitaire.PegSolitaire()
    #     actor = Actor.Actor(0.09)
    #     NN = CriticModules.Net()
    #     critic_module = CriticModules.NNApproximator(NN)
    #     # table = CriticModules.Table(0.09)
    #     critic = Critic.Critic(0.09, critic_module)
    #
    #     print(game)
    #     AC = ActorCritic.ActorCritic(game, actor, critic)
    #     scores = AC.train(2000, 0.99)
    #
    #     # plt.close('all')
    #     plt.plot(list(range(len(scores))), scores)
    #     plt.legend()
    #     plt.show()

    # moves = game.get_legal_moves()
    # game.execute_move(moves[0])
    # Visualize.draw(game.board, triangle=False, last_move=moves[0])




