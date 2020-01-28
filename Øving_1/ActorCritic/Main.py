from ActorCritic import Actor
from ActorCritic import Critic


class ActorCritic:
    def __init__(self, game):
        self.game = game

    def train(self, episodes, discount_factor):
        episode_lengths = []
        epsilon = 0.8
        epsilon_decay = 0.9995
        # Init critic
        critic = Critic.Critic(0.06)
        # Init actor
        actor = Actor.Actor(0.06)
        # For each episode
        for episode in range(episodes):
            print("new episode")
            # init s and a
            self.game.reset()
            curr_state = self.game.get_state()
            curr_action = actor.get_action(curr_state, self.game.get_legal_moves(), epsilon)
            curr_episode = []
            # for each step in episode
            while not self.game.is_finished():
                # do action a in state s, receive reinforcement r
                next_state, reward = self.game.execute_move(curr_action)
                # a':= next action dedicated by policy
                next_action = actor.get_action(next_state, self.game.get_legal_moves(), epsilon)
                # e(s',a') = 1 for actor
                actor.set_eligibility(curr_state, curr_action, 1)
                # critic - temporal difference
                td_error = critic.compute_td_error(curr_state, next_state, reward, discount_factor)
                # e(s') = 1 for critic TODO: s or s'?
                critic.set_eligibility(curr_state, 1)
                curr_episode.append((curr_state, curr_action, td_error))
                # for each state and action in current episode
                for state, action, td_error in curr_episode:
                    # critic value update
                    critic.update_state_value(state, td_error)
                    # critic e update
                    critic.set_eligibility(state, critic.get_eligibility(state))
                    # actor policy update
                    actor.update_state_action_value(state, action, td_error)
                    # actor e update
                    actor.set_eligibility(state, action, actor.get_eligibility(state, action))
                # s:=s'
                curr_state = next_state
                # a:=a'
                curr_action = next_action
            epsilon *= epsilon_decay
            print(episode, len(curr_episode), epsilon)
            episode_lengths.append(len(curr_episode))
        print(actor.sa_values.values())
        return episode_lengths
