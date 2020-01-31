from matplotlib import pyplot as plt

visited = set()


def dfs(game):
    if game.is_finished():
        game.print_board()
        return 1 if game.outcome() == 1 else 0, 1
    if game.get_state() in visited:
        return 0, 0
    else:
        visited.add(game.get_state())

    num_solved = 0
    num_visited = 0
    leg_moves = game.get_legal_moves()
    for move in leg_moves:
        game.execute_move(move)
        temp_solved, temp_visited = dfs(game)
        game.undo_move()
        num_solved += temp_solved
        num_visited += temp_visited
    return num_solved, num_visited


if __name__ == '__main__':
    from Board import PegSolitaire, Visualize
    from ActorCritic import Main as ActorCritic

    game = PegSolitaire.PegSolitaire()
    moves = game.get_legal_moves()
    game.execute_move(moves[0])
    Visualize.draw(game.board, triangle=True, last_move=moves[0])

    input()
    game = PegSolitaire.PegSolitaire()
    game.print_board()
    print(dfs(game))
    #
    # for _ in range(1):
    #     game = PegSolitaire.PegSolitaire()
    #     print(game)
    #     AC = ActorCritic.ActorCritic(game)
    #     scores = AC.train(2000, 0.99)
    #
    #     # plt.close('all')
    #     plt.plot(list(range(len(scores))), scores)
    #     plt.legend()
    #     plt.show()
