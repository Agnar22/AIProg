import numpy as np


class Actor:
    # table that maps state-action pairs to values (should normalize?)
    def __init__(self, learning_rate):
        self.sa_values = {}
        self.sa_eligibilities = {}
        self.lr = learning_rate

    def reset(self):
        self.sa_values = {}
        self.sa_eligibilities = {}

    def get_action(self, state, legal_actions, epsilon):
        state = state[0]
        if len(legal_actions) == 0:
            return None
        if np.random.uniform() < epsilon:
            # print("random action", epsilon)
            return legal_actions[np.random.randint(0, len(legal_actions))]
        # TODO: normalize values?
        values = np.array([self.sa_values.setdefault(state, {}).setdefault(action, 0) for action in legal_actions])
        # print(values)
        return legal_actions[np.argmax(values)]

    def set_eligibility(self, state, action, eligibility):
        self.sa_eligibilities.setdefault(state[0], {})[action] = eligibility

    def get_eligibility(self, state, action):
        return self.sa_eligibilities.setdefault(state[0], {}).setdefault(action, 0)

    def update_state_action_value(self, state, action, td_error):
        sa_value = self.sa_values.setdefault(state[0], {}).setdefault(action, 0)
        self.sa_values[state[0]][action] = sa_value + self.lr * self.get_eligibility(state, action) * td_error
