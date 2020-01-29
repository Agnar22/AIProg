from ActorCritic import Actor
from ActorCritic import Critic


class ActorCritic:
    def __init__(self, game):
        self.game = game

    def train(self, episodes, discount_factor):
        # positions_set = set()
        episode_lengths = []
        epsilon = 0.8
        discount_factor = 0.99
        epsilon_decay = 0.997
        elig_actor = 0.8
        elig_critic = 0.8
        # Init critic
        critic = Critic.Critic(0.09)
        # Init actor
        actor = Actor.Actor(0.09)
        # For each episode
        for episode in range(episodes):
            print("new episode")
            # init s and a
            self.game.reset()
            curr_state = self.game.get_state()
            curr_action = actor.get_action(curr_state, self.game.get_legal_moves(), epsilon)
            curr_episode = []
            # curr_positions_set = set()
            # curr_positions_set.add(str(self.game.get_state()))
            # for each step in episode
            end_rew=None
            while not self.game.is_finished():
                # if episode == episodes - 1:
                #     input()
                #     print(self.game)
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
                #print("Curr episode", *curr_episode[-1])
                # for each state and action in current episode
                for num, [state, action, _] in enumerate(curr_episode):
                    #print(state)
                    """
                    if num==0:
                        print("Reward", reward, "td_error", td_error)
                        print("critic el", critic.get_eligibility(state), "state value", critic.state_values[state]) 
                        print("actor  el", actor.get_eligibility(state, action), " sa value", actor.sa_values.setdefault(state, {}).setdefault(action, 0))
                    """
                    # critic value update
                    critic.update_state_value(state, td_error)
                    # critic e update01
                    critic.set_eligibility(state, elig_critic * discount_factor * critic.get_eligibility(state))
                    # actor policy update
                    actor.update_state_action_value(state, action, td_error)
                    # actor e update
                    actor.set_eligibility(state, action,
                                          elig_actor * discount_factor * actor.get_eligibility(state, action))
                # s:=s'
                curr_state = next_state
                # a:=a'
                curr_action = next_action
                end_rew=reward
                # curr_positions_set.add(self.game.get_state())
            #print(end_rew)
            epsilon *= epsilon_decay
            print(episode, len(curr_episode), epsilon)
            # print("positions {0}, unique positions {1}".format(len(curr_positions_set),len(curr_positions_set.difference(positions_set))))
            # positions_set=positions_set.union(curr_positions_set)
            # print("total_positions", len(positions_set))
            episode_lengths.append(len(curr_episode))
        # print(actor.sa_values.values())
        # print("total_positions", len(positions_set))
        return episode_lengths
