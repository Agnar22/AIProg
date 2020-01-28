

class ActorCritic:
    def __init__(self):
        pass

    def train(self):
        # Init critic
        # Init actor
        # For each episode
        #   init s and a
        #   for each step in episode
        #       do action a in state s, receive reinforcement r
        #       a':= next action dedicated by policy
        #       e(s,a') = 1 for actor
        #       critic - temporal difference
        #       s(s) = 1 for critic
        #       for each state and action in current episode
        #           critic value update
        #           critic e update
        #           actor policy update
        #           actor e update
        #       s:=s'
        #       a:=a'
        pass

class Critic:
    # Can use function approximator (ANN) or table based
    def __init__(self):
        pass

class Actor:
    def __init__(self):
        pass