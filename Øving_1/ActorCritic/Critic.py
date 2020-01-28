import numpy as np


class Critic:
    # Can use function approximator (ANN) or table based
    def __init__(self, learning_rate):
        self.state_values = {}
        self.state_eligibilities = {}
        self.lr = learning_rate

    def compute_td_error(self, from_state, to_state, reward, discount_factor):
        # print(self.state_values.setdefault(from_state, np.random.uniform(-0.1, 0.1)))
        # print(self.state_values.setdefault(to_state, np.random.uniform(-0.1, 0.1)))
        # print(reward, discount_factor)
        return reward + discount_factor * self.state_values.setdefault(to_state, np.random.uniform(-0.1, 0.1)) \
               - self.state_values.setdefault(from_state, np.random.uniform(-0.1, 0.1))

    def set_eligibility(self, state, eligibility):
        self.state_eligibilities[state] = eligibility

    def get_eligibility(self, state):
        return self.state_eligibilities[state]

    def update_state_value(self, state, td_error):
        self.state_values[state] = self.state_values[state] + self.lr * self.state_eligibilities[state] * td_error
