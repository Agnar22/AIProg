class Actor:
    # table that maps state-action pairs to values (should normalize)
    def __init__(self, learning_rate):
        self.sa_values = {}
        self.sa_eligibilities = {}
        self.lr = learning_rate

    def get_best_action(self, state, legal_actions):
        pass

    def set_eligibility(self, state, action, eligibility):
        pass

    def get_eligibility(self, state, action):
        pass

    def update_state_action_value(self, state, action, td_error):
        pass
