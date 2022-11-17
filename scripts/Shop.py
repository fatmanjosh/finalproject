import rospy
from nav_msgs.msg import OccupancyGrid

import numpy as np

class Shop:
    def __init__(self):
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

        # rospy.loginfo(ocuccupancy_map.data)

        map_total = self._map.info.height * self._map.info.width


        # rospy.loginfo(map_total)

        self.grid_map = self.shrink_map()


        self.states = self.generate_states()

        self.States2d = self.generate_2dstates()
        UP = "UP"
        DOWN = "DOWN"
        LEFT = "LEFT"
        RIGHT = "RIGHT"

        self.actions = ("UP", "DOWN", "LEFT", "RIGHT")



        self.possible_transitions = {
            "s0" : [RIGHT],
            "s1" : [LEFT, RIGHT, UP],
            "s2" : [LEFT, RIGHT],
            "s3" : [LEFT, RIGHT, UP],
            "s4" : [LEFT, RIGHT],
            "s5" : [LEFT, RIGHT, UP],
            "s6" : [LEFT, RIGHT],
            "s7" : [LEFT, RIGHT, UP],
            "s8" : [LEFT, RIGHT, UP],
            "s9" : [RIGHT, UP, DOWN],
            "s10" : [LEFT],
            "s11" : [UP, DOWN],
            "s12" : [RIGHT, UP, DOWN],
            "s13" : [LEFT],
            "s14" : [RIGHT, UP, DOWN],
            "s15" : [LEFT, DOWN],
            "s16" : [UP, DOWN],
            "s17" : [RIGHT],
            "s18" : [LEFT, UP, DOWN],
            "s19" : [RIGHT],
            "s20" : [LEFT, UP, DOWN],
            "s21" : [UP, DOWN],
            "s22" : [RIGHT, UP, DOWN],
            "s23" : [LEFT],
            "s24" : [LEFT, UP, DOWN],
            "s25": [LEFT],
            "s26": [UP, DOWN],
            "s27": [RIGHT],
            "s28": [LEFT, UP, DOWN],
            "s29": [RIGHT],
            "s30": [LEFT, UP, DOWN],
            "s31": [RIGHT],
            "s32": [LEFT, UP, DOWN],
            "s33": [UP, DOWN],
            "s34": [UP, DOWN],
            "s35" : [RIGHT,UP,DOWN],
            "s36" : [RIGHT,LEFT,UP],
            "s37" : [RIGHT,LEFT,UP,DOWN],
            "s38" : [RIGHT, LEFT],
            "s39" : [RIGHT, LEFT, UP, DOWN],
            "s40" : [RIGHT,LEFT, UP],
            "s41" : [RIGHT, LEFT, UP, DOWN],
            "s42" : [LEFT],
            "s43" : [RIGHT],
            "s44" : [LEFT, UP, DOWN],
            "s45" : [DOWN],
            "s46" : [UP, DOWN],
            "s47" : [UP, DOWN],
            "s48" : [DOWN],
            "s49" : [UP, DOWN],
            "s50" : [UP, DOWN],
            "s51": [RIGHT, UP, DOWN],
            "s52" : [LEFT],
            "s53" : [UP, DOWN],
            "s54" : [RIGHT, UP, DOWN],
            "s55" : [LEFT],
            "s56" : [RIGHT],
            "s57" : [LEFT, UP, DOWN],
            "s58" : [UP],
            "s59" : [UP, DOWN],
            "s60" : [UP, DOWN],
            "s61" : [UP],
            "s62" : [UP, DOWN],
            "s63" : [RIGHT, UP],
            "s64" : [RIGHT, LEFT, DOWN],
            "s65" : [RIGHT, LEFT, UP, DOWN],
            "s66" : [RIGHT, LEFT, DOWN],
            "s67" : [RIGHT, LEFT, UP],
            "s68": [RIGHT, LEFT, DOWN],
            "s69" : [RIGHT, LEFT, DOWN],
            "s70" : [RIGHT, LEFT, UP, DOWN],
            "s71" : [LEFT, UP],
            "s72" : [DOWN],
            "s73" : [DOWN],
            "s74": [DOWN],
            "s75": [DOWN],
            "s76": [DOWN]
        }

        self.transitions = {
            RIGHT : self.transition_states(RIGHT, 1, 0),
            LEFT : self.transition_states(LEFT, -1, 0),
            UP : self.transition_states(UP, 0, 1),
            DOWN : self.transition_states(DOWN, 0, -1)
        }

        self.rewards = self.generate_rewards()
        self.rewards2d = self.generate_2drewards()

        # print(self.transitions)

        self.value_iteration()







    def generate_states(self):
        possible_states = {}
        state_no = "s"
        i = 0
        for row in range(11):
            for col in range(9):
                if self.grid_map[row][col] == 0:
                    possible_states[str(state_no) + str(i)] = (col, row)
                    i += 1

        return possible_states

    def generate_2dstates(self):
        possible_states = []
        state_no = "s"
        i = 0
        for row in range(99):
            if self.grid_map[row] == 0:
                possible_states.append(i)
                i += 1

        return possible_states

    def generate_rewards(self):
        rewards = {}
        state_no = "s"
        i = 0
        for row in range(11):
            for col in range(9):
                if self.grid_map[row][col] == 0:
                    rewards[str(state_no) + str(i)] = -1
                    i += 1
        return rewards

    def generate_2drewards(self):
        rewards = []
        state_no = "s"
        i = 0
        for row in range(99):
                if self.grid_map[row] == 0:
                    rewards.append(-1)
                    i += 1
        return rewards

        # return possible_states

# i = 0
# for row in range(11):
#     string = ""
#     state_no = "s"
#
#     for col in range(9):
#         if self.grid_map[row][col] == 100:
#             string += " -  "
#         else:
#             string += state_no + str(i) + " "
#             possible_states[str(state_no) + str(i) ] = (col, row)
#             i += 1
#     print(string)

# print(possible_states)

# return possible_states




    def shrink_map(self):
        # y = 0
        # new_map = [[]]
        # should_be = [[0, 100, 0, 100, 0, 100, 100, 0, 0],
        #                   [0, 0, 0, 0, 0, 0,0,0,0],
        #                   [0,0,0,0,100,0,0,0,100],
        #                   [100,0,100,0,0,0,100,0],
        #                   [0,0,0,0,100,0,0,0,100],
        #                   [100,0,0,0,0,0,0,0,0],
        #                   [0,0,0,0,100,0,100,0,100],
        #                   [100,0,0,0,0,0,0,0,100],
        #                   [100,0,0,0,0,0,100,0,100],
        #                   [100,0,0,0,100,0,0,0,0],
        #                   [0,0,0,0,0,0,0,0,0,0]]
        #
        map_total = self._map.info.height * self._map.info.width
        new_map = []

        new2d = []
        for row in range(3, self._map.info.height, 7):
            for col in range(3, self._map.info.width, 7):
                new2d.append(self._map_data[col + row * 63])


        for row1 in range(11):
            st = " "
            temp= []
            for col1 in range(9):
                temp.append(new2d[col1 + row1 * 9])
            new_map.append(temp)


        return new_map






        # temp = np.reshape(new2d, (9, 11))



    def transition_states(self, direction, x, y):
        # up
        transition_dict = {}
        for state in self.states:
            # print(state)
            # print(self.possible_transitions[state])
            transition_dict[state] = {}
            # print("\n\n\n\n")
            # print(transition_dict)
            for internal_state in self.states:
                # print(f"internal {internal_state}")
                # print(f"state {state}")
                if internal_state == state:
                    if not direction in self.possible_transitions[state]:
                        transition_dict[state][internal_state] = 1
                    else:
                        transition_dict[state][internal_state] = 0.2
                elif direction in self.possible_transitions[state]\
                        and self.states[state][0] + x == self.states[internal_state][0]\
                        and self.states[state][1] + y == self.states[internal_state][1]:
                            transition_dict[state][internal_state] = 0.8
                else:
                    transition_dict[state][internal_state] = 0

        return transition_dict
                # else:
                #     transition_dict[state][internal_state] = 0


        # for statey, valuey in transition_dict.items():
        # print(f"{statey} : {valuey}\n")

        # print(transition_dict)


    # def value_iteration(self):
    #     # Initialize Markov Decision Process model
    #     actions = self.actions  # actions (0=left, 1=right)
    #     states = self.States2d  # states (tiles)
    #     rewards = self.rewards2d  # Direct rewards per state
    #     gamma = 0.9  # discount factor
    #     # Transition probabilities per state-action pair
    #     probs = self.transitions
    #
    #     # Set value iteration parameters
    #     max_iter = 10000  # Maximum number of iterations
    #     delta = 1e-400  # Error tolerance
    #     V = [0] * 77 # Initialize values
    #     pi = [None] * 77 # Initialize policy
    #
    #     # Start value iteration
    #     for i in range(max_iter):
    #         max_diff = 0  # Initialize max difference
    #         V_new = [0] * 77  # Initialize values
    #         for s in states:
    #             max_val = 0
    #             for a in actions:
    #
    #                 # Compute state value
    #                 val = rewards[s]  # Get direct reward
    #                 for s_next in states:
    #                     val += probs[a][s][s_next] * (
    #                             gamma * V[s_next]
    #                     )  # Add discounted downstream values
    #
    #                 # Store value best action so far
    #                 max_val = max(max_val, val)
    #
    #                 # Update best policy
    #                 if V[s] < val:
    #                     pi[s] = a  # Store action with highest value
    #
    #             V_new[s] = max_val  # Update value with highest value
    #
    #             # Update maximum difference
    #             max_diff = max(max_diff, abs(V[s] - V_new[s]))
    #
    #         # Update value functions
    #         V = V_new
    #
    #         # If diff smaller than threshold delta for all states, algorithm terminates
    #         if max_diff < delta:
    #             break
    #
    #     print(V)






if __name__ == '__main__':
    # --- Main Program  ---
    rospy.init_node("map_tester")
    node = Shop()
    rospy.spin()