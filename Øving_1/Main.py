
if __name__ == '__main__':
    from Board import PegSolitaire
    from ActorCritic import Main as ActorCritic

    game = PegSolitaire.PegSolitaire()
    print(game)
    AC = ActorCritic.ActorCritic(game)
    AC.train(4, 0.99)