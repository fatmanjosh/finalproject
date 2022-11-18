# uncomment thbis to run on termnial
"""
import rospy
from nav_msgs.msg import OccupancyGrid
"""


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

        ################################################################################################################
        self.grid_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [100, 0, 0, 0, 100, 0, 0, 0, 0],
                         [100, 0, 0, 0, 0, 0, 100, 0, 100],
                         [100, 0, 0, 0, 0, 0, 0, 0, 100],
                         [0, 0, 0, 0, 100, 0, 100, 0, 100],
                         [100, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 100, 0, 0, 0, 100],
                         [100, 0, 100, 0, 0, 0, 100, 0, 0],
                         [0, 0, 0, 0, 100, 0, 0, 0, 100],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 100, 0, 100, 0, 100, 100, 0, 0]]

        self.states =\
            {'s0': (0, 0), 's1': (1, 0), 's2': (2, 0), 's3': (3, 0), 's4': (4, 0), 's5': (5, 0), 's6': (6, 0), 's7': (7, 0),
         's8': (8, 0), 's9': (1, 1), 's10': (2, 1), 's11': (3, 1), 's12': (5, 1), 's13': (6, 1), 's14': (7, 1),
         's15': (8, 1), 's16': (1, 2), 's17': (2, 2), 's18': (3, 2), 's19': (4, 2), 's20': (5, 2), 's21': (7, 2),
         's22': (1, 3), 's23': (2, 3), 's24': (3, 3), 's25': (4, 3), 's26': (5, 3), 's27': (6, 3), 's28': (7, 3),
         's29': (0, 4), 's30': (1, 4), 's31': (2, 4), 's32': (3, 4), 's33': (5, 4), 's34': (7, 4), 's35': (1, 5),
         's36': (2, 5), 's37': (3, 5), 's38': (4, 5), 's39': (5, 5), 's40': (6, 5), 's41': (7, 5), 's42': (8, 5),
         's43': (0, 6), 's44': (1, 6), 's45': (2, 6), 's46': (3, 6), 's47': (5, 6), 's48': (6, 6), 's49': (7, 6),
         's50': (1, 7), 's51': (3, 7), 's52': (4, 7), 's53': (5, 7), 's54': (7, 7), 's55': (8, 7), 's56': (0, 8),
         's57': (1, 8), 's58': (2, 8), 's59': (3, 8), 's60': (5, 8), 's61': (6, 8), 's62': (7, 8), 's63': (0, 9),
         's64': (1, 9), 's65': (2, 9), 's66': (3, 9), 's67': (4, 9), 's68': (5, 9), 's69': (6, 9), 's70': (7, 9),
         's71': (8, 9), 's72': (0, 10), 's73': (2, 10), 's74': (4, 10), 's75': (7, 10), 's76': (8, 10)}
        ################################################################################################################
        UP = "UP"
        DOWN = "DOWN"
        LEFT = "LEFT"
        RIGHT = "RIGHT"

        self.actions = ("UP", "DOWN", "LEFT", "RIGHT")



        """
        all possible actions from each state
        """
        self.possible_transitions = {
            "s0" : ["TERMINAL"],## changes here to add terminal states
            # "s0": [RIGHT],
            "s1" : [LEFT, RIGHT, UP],
            "s2" : [LEFT, RIGHT],
            "s3" : [LEFT, RIGHT, UP],
            "s4" : [LEFT, RIGHT],
            "s5" : [LEFT, RIGHT, UP],
            # "s6" : [LEFT, RIGHT],
            "s6": ["TERMINAL"],## changes here to add terminal states
            "s7" : [LEFT, RIGHT, UP],
            "s8" : [LEFT, RIGHT, UP],
            "s9" : [RIGHT, UP, DOWN],
            "s10" : [LEFT],
            "s11" : [UP, DOWN],
            # "s12" : [RIGHT, UP, DOWN],
            "s12": ["TERMINAL"],
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

        """
        All possible transitions in the format:
        ACTION : {INITIAL STATE : {NEXT STATE : PROBABILITY OF TRANSITION}}
        
        EG:= {RIGHT : {s0 : {s0 : 1, s1 : 0...}, s1 : {s0 : {s0 : 0, s1 : 0.2, ...}}}, LEFT : {...}}
        """
        self.transitions = {
            RIGHT : self.transition_states(RIGHT, 1, 0),
            LEFT : self.transition_states(LEFT, -1, 0),
            UP : self.transition_states(UP, 0, 1),
            DOWN : self.transition_states(DOWN, 0, -1)
        }



        self.rewards = self.generate_rewards()

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
        # print(possible_states)
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
        # adding specific rewards for specific states
        rewards.update({"s0": 100})
        rewards.update({"s6": -100})

        return rewards

    def shrink_map(self):
        """
        :return: generates new map made from the centers of our cells
        """
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
            temp= []
            for col1 in range(9):
                temp.append(new2d[col1 + row1 * 9])
            new_map.append(temp)

        return new_map






        # temp = np.reshape(new2d, (9, 11))



    def transition_states(self, direction, x, y):
        """
        calculates transition matrix given probabilities

        :param direction: direction of movement
        :param x: what to add to the x axis to go in that direction
        :param y: what to add to the x axis to go in that direction
        :return: transition probabilities dictionary
        """
        transition_dict = {}
        for state in self.states:
            transition_dict[state] = {}
            for next_state in self.states:
                if next_state == state: # if the next state and the start state are the same
                    if not direction in self.possible_transitions[state]:# if you cant move in that direction from state
                        transition_dict[state][next_state] = 1   # stay where you are
                    else:
                        transition_dict[state][next_state] = 0.2 # otherwise you have a probability of not moving 0.2
                elif direction in self.possible_transitions[state]\
                        and self.states[state][0] + x == self.states[next_state][0]\
                        and self.states[state][1] + y == self.states[next_state][1]: #if you can go in the direction
                            transition_dict[state][next_state] = 0.8                 #and if the state in the direction
                else:                                                                #is the next state then prob is 0.8
                    transition_dict[state][next_state] = 0 # if you can t go there then probability 0

        return transition_dict



    def calc_state_string(self, sx, sy):
        return "s" + str(sx + sy * 11)

    def state_int(self, x, y):
        return x + y * 11



    def value_iteration(self):
        # Initialize Markov Decision Process model
        actions = self.actions  # actions (0=left, 1=right)
        states = self.states  # states (tiles)
        rewards = self.rewards# Direct rewards per state
        gamma = 0.9  # discount factor
        # Transition probabilities per state-action pair
        probs = self.transitions

        # Set value iteration parameters
        max_iter = 10000  # Maximum number of iterations
        delta = 1e-20# Error tolerance

        V = {}
        pi = {}
        for state in states:
            V[state] = 0 # Initialize values
            pi[state] = "None" # Initialize policy


        # Start value iteration
        for i in range(max_iter):
            max_diff = 0  # Initialize max difference
            V_new = {}
            for s in states:
                V_new[s] = 0
                max_val = 0
                for a in actions:
                    # Compute state value
                    val = rewards[s]  # Get direct reward
                    for s_next in states:
                        val += probs[a][s][s_next] * (gamma * V[s_next]) # Add discounted downstream values

                    # Store value best action so far
                    max_val = max(max_val, val)

                    # Update best policy
                    if V[s] < val:
                        if not self.possible_transitions[s] == ["TERMINAL"]: # if you can't transition then no pi update
                            pi[s] = a # Store action with highest value

                V_new.update({s : max_val})  # Update value with highest value

                # Update maximum difference
                max_diff = max(max_diff, abs(V[s] - V_new[s]))

            # Update value functions
            V = V_new

            # If diff smaller than threshold delta for all states, algorithm terminates
            if max_diff < delta:
                break
        print(V)

        print(pi)



# have if name commented to run in  your ide so you can debug
# have Shop commented to run on terminal
###################################
"""
# if __name__ == '__main__':
#     # --- Main Program  ---
#     rospy.init_node("map_tester")
#     node = Shop()
#     rospy.spin()
"""
#################################################
node = Shop()
################################################