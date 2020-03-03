class ActorCritic:
    def __init__(self, game, actor, critic):
        self.game = game
        self.actor = actor
        self.critic = critic

    def train(self, episodes, param, visualization):
        episode_lengths = []
        epsilon = param['epsilon']
        epsilon_decay = param['epsilon_decay']
        disc_actor = param['disc_actor']
        disc_critic = param['disc_critic']
        elig_actor = param['elig_decay_actor']
        elig_critic = param['elig_decay_critic']
        # Init critic
        self.critic.reset()
        # Init actor
        self.actor.reset()
        # For each episode
        for episode in range(episodes):
            print("new episode", episode)
            self.run_episode(epsilon, disc_actor, disc_critic, elig_actor, elig_critic, episode_lengths)
            epsilon *= epsilon_decay
            if param['display_time'] < episode:
                visualization(param, self.game, self.actor)

        return episode_lengths

    def run_episode(self, epsilon, disc_actor, disc_critic, elig_actor, elig_critic, episode_lengths):
        # init s and a
        self.game.reset()
        curr_state = self.game.get_state()
        curr_action = self.actor.get_action(curr_state, self.game.get_legal_moves(), epsilon)
        curr_episode = []
        # for each step in episode
        while not self.game.is_finished():
            # do action a in state s, receive reinforcement r
            next_state, reward = self.game.execute_move(curr_action)
            # a':= next action dedicated by policy
            next_action = self.actor.get_action(next_state, self.game.get_legal_moves(), epsilon)
            # e(s,a) = 1 for actor
            self.actor.set_eligibility(curr_state, curr_action, 1)
            # critic - temporal difference
            td_error_actor = self.critic.compute_td_error(curr_state, next_state, reward, disc_actor,
                                                          finished=self.game.is_finished())
            td_error_critic = self.critic.compute_td_error(curr_state, next_state, reward, disc_critic,
                                                           finished=self.game.is_finished())
            # e(s) = 1 for critic
            self.critic.set_eligibility(curr_state, 1)

            curr_episode.append((curr_state, curr_action, td_error_actor, td_error_critic))
            # print("error1 ", td_error_actor)

            # for each state and action in current episode
            for num, [state, action, *_] in enumerate(curr_episode):
                # critic value update
                self.critic.update_state_value(state, td_error_critic, after=(num + 1 == len(curr_episode)))
                # self.critic.update_state_value(state, td_error_critic, after=False)
                # critic e update
                self.critic.set_eligibility(state, elig_critic * disc_critic * self.critic.get_eligibility(state))
                # actor policy update
                self.actor.update_state_action_value(state, action, td_error_actor)
                # actor e update
                self.actor.set_eligibility(state, action,
                                           elig_actor * disc_actor * self.actor.get_eligibility(state, action))
            # s:=s'
            curr_state = next_state
            # a:=a'
            curr_action = next_action
        print("End", len(curr_episode), epsilon)
        episode_lengths.append((self.game.get_state()[1] == 1).sum())
