class Critic:

    def __init__(self, value_approximator):
        self.value_approximator = value_approximator

    def reset(self):
        self.value_approximator.reset()

    def compute_td_error(self, from_state, to_state, reward, discount_factor, finished=False):
        current_value = self.value_approximator.predict(from_state)
        if finished:
            return reward - current_value
        target_value = reward + discount_factor * self.value_approximator.predict(to_state)
        td_error = target_value - current_value
        return td_error

    def set_eligibility(self, state, eligibility):
        self.value_approximator.set_eligibility(state, eligibility)

    def get_eligibility(self, state):
        return self.value_approximator.get_eligibility(state)

    def update_state_value(self, state, td_error, after=False):
        self.value_approximator.fit(state, td_error, after=after)
