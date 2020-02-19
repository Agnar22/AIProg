class Critic:

    def __init__(self, value_approximator):
        self.value_approximator = value_approximator

    def reset(self):
        self.value_approximator.reset()

    def compute_td_error(self, from_state, to_state, reward, discount_factor, finished=False):
        # target_value = reward + discount_factor * self.state_values.setdefault(to_state, np.random.uniform(-0.01, 0.01))
        current_value = self.value_approximator.predict(from_state)
        if finished:

            # print("Last", reward, current_value, reward - current_value)
            return reward - current_value
        target_value = reward + discount_factor * self.value_approximator.predict(to_state)
        # current_value = self.state_values.setdefault(from_state, np.random.uniform(-0.01, 0.01))
        td_error = target_value - current_value
        return td_error

    def set_eligibility(self, state, eligibility):
        self.value_approximator.set_eligibility(state, eligibility)

    def get_eligibility(self, state):
        return self.value_approximator.get_eligibility(state)

    def update_state_value(self, state, td_error):
        # self.state_values[state] = self.state_values[state] + self.lr * self.state_eligibilities[state] * td_error
        self.value_approximator.fit(state, td_error)
