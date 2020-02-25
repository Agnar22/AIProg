from Games.Nim import Main as Nim
from Games.Ledge import Main as Ledge
from MCTS import Main as MCTS

if __name__ == '__main__':
    # TODO: is store state and load state working correctly?
    # game = Nim.Nim(11, 3)
    game = Ledge.Ledge("01002")
    mcts = MCTS.MCTS()
    # mcts.search(game, 200)

    while not game.is_finished():
        state = game.get_state()[0]
        mcts.search(game, 500)
        print(mcts.get_search_statistics(state))
        print("move", mcts.get_recommended_move(state))
        game.execute_move(mcts.get_recommended_move(state))
        mcts.reset()
    print(game.outcome())
