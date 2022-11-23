#!/usr/bin/env python
import random
import rospy
import map, transitions, heatmap

class Shop:
    def __init__(self):
        
        self.states = map.states()
        self.possible_transitions = map.possible_transitions()
        self.transitions = transitions.transitions()
        self.rewards = self.generate_rewards()

        self.policy_iteration()


    def generate_rewards(self):
        rewards = {}
        state_no = "s"
        i = 0
        for row in range(11):
            for col in range(9):
                if map.grid_map()[row][col] == 0:
                    rewards[str(state_no) + str(i)] = -1
                    i += 1
        # adding specific rewards for specific states
        rewards.update({"s0": 100})
        rewards.update({"s6": -100})

        return rewards


    def policy_iteration(self):
        # Initialize Markov Decision Process model
        actions = map.actions() # actions (0=left, 1=right)
        states = map.states()   # states (tiles)
        rewards = self.rewards  # Direct rewards per state
        gamma = 0.9             # discount factor
        # Transition probabilities per state-action pair
        probs = self.transitions = transitions.transitions()

        # Set value iteration parameters
        max_policy_iter = 10000     # Maximum number of iterations
        max_value_iter = 10000
        delta = 1e-20               # Error tolerance

        V = {}
        pi = {}
        for state in states:
            V[state] = 0    # Initialize values
            pi[state] = random.choice(self.possible_transitions[state]) # Initialize 

        for i in range(max_policy_iter):
            # Initial assumption: policy is stable
            optimal_policy_found = True

            # Policy evaluation
            # Compute value for each state under current policy
            for j in range(max_value_iter):
                max_diff = 0    # Initialize max difference
                for s in states:
                    #print(s + " and " + str(self.possible_transitions[s]))
                    # Compute state value
                    val = rewards[s]  # Get direct reward
                    for s_next in states:
                        val += probs[pi[s]][s][s_next] * (
                                gamma * V[s_next]
                        )  # Add discounted downstream values

                    # Update maximum difference
                    max_diff = max(max_diff, abs(val - V[s]))

                    V[s] = val  # Update value with highest value
                # If diff smaller than threshold delta for all states, algorithm terminates
                if max_diff < delta:
                    break

            # Policy iteration
            # With updated state values, improve policy if needed
            for s in states:
                #print(s)
                if self.possible_transitions[s] == ["TERMINAL"]:
                   pi[s] = "TERMINAL"
                val_max = V[s]
                for a in actions:
                    val = rewards[s]  # Get direct reward
                    for s_next in states:
                        val += probs[a][s][s_next] * (
                            gamma * V[s_next]
                        )  # Add discounted downstream values

                    # Update policy if (i) action improves value and (ii) action different from current policy
                    #if self.possible_transitions[s] == ["TERMINAL"]:
                    #        pi[s] = "TERMINAL"
                    if val > val_max and pi[s] != a:
                            pi[s] = a
                            val_max = val
                            optimal_policy_found = False

            # If policy did not change, algorithm terminates
            if optimal_policy_found:
                break
           
        print(V)

        print(pi)

if __name__ == '__main__':

    rospy.init_node("map_tester")
    node = Shop()
    rospy.spin()


