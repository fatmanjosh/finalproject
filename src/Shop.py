#!/usr/bin/env python3
import random
import rospy
from heatmap import heatmap
import map, transitions
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import PoseArray, Pose, Point


class Shop:
    def __init__(self, boxes):
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


        self.box_states = self.generate_box_states(boxes)
        self.boxes_to_visit = {}
        
        self.NUM_OF_PEOPLE = 50
        self.heatmap = heatmap(self.NUM_OF_PEOPLE, self.box_states)  # TODO: should this use boxes_to_visit rather than all boxes across map?

        self.policy_pub = rospy.Publisher("/policy", PoseArray, queue_size = 100)
        self.pi_transitions = {}
        self.pi_values = {}
        self.states = map.states()
        self.possible_transitions = map.possible_transitions()
        self.actions = map.actions()
        self.people = self.heatmap.stateUncertainty(0)
        self.transitions = transitions.transitions(self.people)

        # should these only be done after robot has been given a list of items to pick up?
        # seems pointless doing it when Shop is initialised, and then again when the robot has a list of items
        self.rewards = self.generate_rewards()
        # self.policy_iteration()
        self.people = self.set_people(self.NUM_OF_PEOPLE)
        self.transitions = transitions.transitions(self.people)
        print(f"\n{sorted(self.people)}")
        self.policy_iteration()

        self.point_pub = rospy.Publisher("/pcloud", PointCloud, queue_size = 100)
        self.box_pub = rospy.Publisher("/boxes", PointCloud, queue_size = 100)
        self.box_to_visit_pub = rospy.Publisher("/boxes_to_visit", PointCloud, queue_size = 100)
    

        self.publish_people()
        
    def set_people(self, number_of_people):
        return self.heatmap.stateUncertainty(1)            

    def show_policy(self):
        arrows = []
        for state, policy in self.pi_transitions.items():
            arrow = Pose()

            # print(policy)

            if(policy == "TERMINAL"):
                continue
            elif (policy == "RIGHT"):
                arrow.orientation.w = -1
                arrow.orientation.z = 0
            elif (policy == "LEFT"):
                arrow.orientation.w = 0
                arrow.orientation.z = 1
            elif (policy == "UP"):
                arrow.orientation.w = -1
                arrow.orientation.z = -1
            elif(policy == "DOWN"):
                arrow.orientation.w = 1
                arrow.orientation.z = -1


            arrow.position.x = map.states()[state][0] * 7 + 4
            arrow.position.y = map.states()[state][1] * 7 + 4

            arrows.append(arrow)
            # print(arrows)

        total = PoseArray()
        total.header.frame_id = "map"
        total.poses= arrows
        self.policy_pub.publish(total)
        # print("published")



    def publish_people(self):
        point_array = PointCloud()
        # people = sorted(self.people)
        people = self.people
        for i in range(len(people)):
            x, y = map.states()[f"s{people[i]}"]
            point = Point()
            point.x = random.gauss(x * 7 + 4, 0.5)

            point.y = random.gauss(y * 7 + 4, 0.5)


            # point.position.x = x * 7 + 4
            # point.position.y = y * 7 + 4
            point_array.points.append(point)
            point_array.header.frame_id = "map"
        r = rospy.Rate(5)
        # self.point_pub.publish(point_array)
        # r.sleep()
        # print("point")

        r.sleep()
        self.point_pub.publish(point_array)
        r.sleep()

    def publish_boxes(self):
        point_array = PointCloud()
        for state in self.box_states.keys():  # TODO: is this meant to show all boxes or only boxes robot is going to? if the latter then may need to be edited
            point = Point()
            x, y = map.states()[state]
            point.x = x * 7 + 4

            point.y = y * 7 +4

            # point.position.x = x * 7 + 4
            # point.position.y = y * 7 + 4
            point_array.points.append(point)
            point_array.header.frame_id = "map"
        r = rospy.Rate(5)
        # self.point_pub.publish(point_array)
        # r.sleep()
        # print("point")

        r.sleep()
        self.box_pub.publish(point_array)
        r.sleep()
        
    def publish_boxes_to_visit(self):
        point_array = PointCloud()
        
        if len(self.boxes_to_visit.keys()) == 0:
            point = Point()
            point.x = 0
            point.y = 0
            point.z = 10000
            point_array.points.append(point)

        
        for state in self.boxes_to_visit.keys():  # TODO: is this meant to show all boxes or only boxes robot is going to? if the latter then may need to be edited
            point = Point()
            x, y = map.states()[state]
            point.x = x * 7 + 4

            point.y = y * 7 + 4

            # point.position.x = x * 7 + 4
            # point.position.y = y * 7 + 4
            point_array.points.append(point)
        r = rospy.Rate(5)
        # self.point_pub.publish(point_array)
        # r.sleep()
        # print("point")
        point_array.header.frame_id = "map"


        r.sleep()
        # print(point_array)
        self.box_to_visit_pub.publish(point_array)
        r.sleep()


    def get_box_states(self):
        return self.box_states

    def generate_box_states(self, boxes):
        # randomly allocate boxes to states along aisles in the map
        possible_box_locations = [10, 13, 17, 19, 23, 25, 27, 29, 31, 42, 43, 45, 48, 52, 55, 56, 58, 61, 72, 73, 74, 75, 76]
        box_states = {}
        for box in boxes:
            selected_state = random.choice(possible_box_locations)  # pick random state from list
            possible_box_locations.remove(selected_state)  # remove state from list
            box_states["s" + str(selected_state)] = box  # add state to a dictionary with the box contents
            print(f"{selected_state} : {box}")

        return box_states

    def update_box_states(self, state):
        # removes the box in given state and sets its reward to -1
        # TODO update to use boxes to visit format
        self.box_states.pop(state)
        self.publish_boxes()


    def print_box_states(self):
        # print the locations of all boxes
        print("all boxes: ")
        for state, box in self.box_states.items():
            print(f"{state} : {box}")

    def set_boxes_to_visit(self, goal_ingredients, boxes):
        # finds the list of boxes that the robot should visit to collect all ingredients
        for box in boxes:
            for ingredient in goal_ingredients:
                if ingredient in box.get_available_ingredients().keys():
                    # get the state number of the box containing this item
                    state_no = list(self.get_box_states().keys())[list(self.get_box_states().values()).index(box)]
                    self.boxes_to_visit[state_no] = box.get_name()  # add state and box name to dictionary
                    break

        self.add_new_box_rewards(self.boxes_to_visit.keys())  # set box rewards to +100

    def update_boxes_to_visit(self, state):
        # removes the box in given state and sets its reward to -1 before publishing the remaining boxes
        self.boxes_to_visit.pop(state)
        self.clear_box_rewards(state)
        self.publish_boxes_to_visit()      
        
    def print_boxes_to_visit(self):
        # prints remaining music
        print(f"\nremaining boxes: {self.boxes_to_visit} \n")

    def generate_rewards(self):
        # initially sets rewards of all cells in map to -1
        # specific cell s6 given -100 reward as it should not be visited
        # returns results in reward dictionary
        rewards = {}
        state_no = "s"
        i = 0
        for row in range(11):
            for col in range(9):
                if map.grid_map()[row][col] == 0:
                    state = str(state_no) + str(i)
                    # if(state in self.box_states.keys()):
                    #     rewards[state] = 100
                    # else:
                    #     rewards[state] = -1
                    rewards[state] = -1
                    i += 1
        rewards.update({"s0": -100})  # program ends when robot moves into s8 so set this to -100 whilst collecting items
        # print(rewards)
        # adding specific rewards for specific states
        # rewards.update({"s0": 100})
        # rewards.update({"s6": -100})

        return rewards

    def set_path_to_customer(self):
        # used to set reward of s8 to 100 and return to customer once all boxes have been visited
        self.rewards.update({"s8" : 100})
        print("\n\nReturning to customer\n\n")
        self.policy_iteration()

    def add_new_box_rewards(self, list_of_states):
        # used to add a reward of +100 to every box in the given list
        for state in list_of_states:
            self.rewards.update({state : 100})
        self.policy_iteration()

    def clear_box_rewards(self, state):
        # used to set reward of a box state to -1 once it has been visited
        self.rewards.update({state : -1})
        self.policy_iteration()

    def policy_iteration(self):
        # Initialize Markov Decision Process model
        actions = self.actions  # actions (0=left, 1=right)
        states = self.states  # states (tiles)
        rewards = self.rewards  # Direct rewards per state
        gamma = 0.9  # discount factor
        # Transition probabilities per state-action pair
        probs = self.transitions

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

        # print(V)
        # print(f"policy{}")
        # k = probs["RIGHT"]["s5"]
        # print(f"transitions{k}")
        self.pi_values = V
        self.pi_transitions = pi

        self.show_policy()

