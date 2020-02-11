class Critic:

    def __init__(self, learning_rate, value_approximator):
        self.state_values = {}
        self.state_eligibilities = {}
        self.lr = learning_rate
        self.value_approximator = value_approximator

    def compute_td_error(self, from_state, to_state, reward, discount_factor):
        target_value = reward + discount_factor * self.value_approximator.predict(to_state)
        # target_value = reward + discount_factor * self.state_values.setdefault(to_state, np.random.uniform(-0.01, 0.01))
        current_value = self.value_approximator.predict(from_state)
        # current_value = self.state_values.setdefault(from_state, np.random.uniform(-0.01, 0.01))
        td_error = target_value - current_value
        return td_error

    def set_eligibility(self, state, eligibility):
        self.state_eligibilities[state] = eligibility

    def get_eligibility(self, state):
        return self.state_eligibilities[state]

    def update_state_value(self, state, td_error, target):
        # self.state_values[state] = self.state_values[state] + self.lr * self.state_eligibilities[state] * td_error
        self.value_approximator.fit(state, td_error, target)
