#!/usr/bin/env python3
import random
import rospy
import map, transitions, heatmap

class Shop:
    def __init__(self):
        # comment the top block to run in ide for debugging
        # comment the bottom block to run on ide
        ##############################################################
        """
        rospy.loginfo("Waiting for a map...")
        try:
            ocuccupancy_map = rospy.wait_for_message("/map", OccupancyGrid, 20)
        except:
            rospy.logerr("Problem getting a map. Check that you have a map_server"
                            " running: rosrun map_server map_server <mapname> ")
            sys.exit(1)
        rospy.loginfo("Map received. %d X %d, %f px/m." %
                        (ocuccupancy_map.info.width, ocuccupancy_map.info.height,
                        ocuccupancy_map.info.resolution))
        # rospy.loginfo(ocuccupancy_map.data)
        self._map = ocuccupancy_map
        self._map_data = ocuccupancy_map.data
        self. debug_map =
        rospy.loginfo(ocuccupancy_map.data)
        map_total = self._map.info.height * self._map.info.width
        rospy.loginfo(map_total)
        self.grid_map = self.shrink_map()
        self.states = self.generate_states()
        """
        self.states = map.states()
        self.possible_transitions = map.possible_transitions()
        self.actions = map.actions()
        self.people = heatmap.heatmap.stateUncertenty(0)
        self.transitions = transitions.transitions(self.people)
        self.rewards = self.generate_rewards()
        self.policy_iteration()
        self.people = heatmap.heatmap.stateUncertenty(100)
        self.transitions = transitions.transitions(self.people)
        print (sorted(self.people))
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
        actions = self.actions  # actions (0=left, 1=right)
        states = self.states  # states (tiles)
        rewards = self.rewards  # Direct rewards per state
        gamma = 0.9  # discount factor
        # Transition probabilities per state-action pair
        probs = self.transitions

        # print(probs)

        # Set value iteration parameters
        max_policy_iter = 10000  # Maximum number of iterations
        max_value_iter = 10000
        delta = 1e-20  # Error tolerance

        V = {}
        pi = {}
        for state in states:
            V[state] = 0  # Initialize values
            pi[state] = random.choice(self.possible_transitions[state])  # Initialize policy

        for i in range(max_policy_iter):
            # Initial assumption: policy is stable
            optimal_policy_found = True

            # Policy evaluation
            # Compute value for each state under current policy
            for j in range(max_value_iter):
                max_diff = 0  # Initialize max difference
                for s in states:
                    # print(s + " and " + str(self.possible_transitions[s]))
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
                # print(s)
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
                    # if self.possible_transitions[s] == ["TERMINAL"]:
                    #        pi[s] = "TERMINAL"
                    if val > val_max and pi[s] != a:
                        pi[s] = a
                        val_max = val
                        optimal_policy_found = False

            # If policy did not change, algorithm terminates
            if optimal_policy_found:
                break

            # print(i)

        print(V)

        print(pi)



if __name__ == '__main__':

    rospy.init_node("map_tester")
    node = Shop()
    rospy.spin()
