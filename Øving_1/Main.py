from matplotlib import pyplot as plt

if __name__ == '__main__':
    from Board import PegSolitaire
    from ActorCritic import Main as ActorCritic

    game = PegSolitaire.PegSolitaire()
    print(game)
    AC = ActorCritic.ActorCritic(game)
    scores = AC.train(4000, 0.99)

    plt.close('all')
    plt.plot(list(range(len(scores))), scores)
    plt.legend()
    plt.show()
