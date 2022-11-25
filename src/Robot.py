#!/usr/bin/env python

import math
from time import perf_counter_ns
import rospy
from geometry_msgs.msg import Twist, Point, PoseWithCovarianceStamped, Pose
from math import atan2, pi
from nav_msgs.msg import Odometry

class Robot:
    def __init__(self, goal_ingredients, replacements):
        self._mover = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self._robot_publisher = rospy.Publisher('/robot_location', PoseWithCovarianceStamped, queue_size=10)
        self._listener = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.newOdom)
        # rospy.init_node('mover', anonymous=True)
        self._goal_ingredients = goal_ingredients
        self._inventory = []
        self._out_of_stock = ["milk", "almond milk"]
        self._replacements = self.update_food_dictionary(replacements)
        self._facing = "RIGHT"
        self._location = "s8"


        # oat milk : almond milk -- mapping oat to almond as an alternative

    # def check_if_at_box(self):
    #     if

    def get_location(self):
        return self._location

    def check_if_at_box(self, box_states):
        if(self._location in box_states):
            return True
        return False

    def update_food_dictionary(self, replacements):
        """
        :param replacements in the form [a, b, c]:
        :return: replacements in the form [a:b, b:c]
        """
        result = {}
        print(replacements)
        for i in range(len(replacements)):
            if i != len(replacements) - 1:
                result.update({replacements[i]: replacements[i + 1]})
        print(result)

        return result

    def newOdom(self, msg):
        # pass
        global x
        global y
        global theta

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        theta = msg.pose.pose.orientation.z
        print(x + " " + y)

        print("\n\n\n\n looooooooool \n\n\n\n\n\n")

    def move_using_policy_iteration(self, states_dict, policy_iteration_transitions):
        # states_dict will need to be passed in from map.states()
        # policy_iteration_transitions will need to be passed in from Shop.get_pi_transitions()
        current_state = self._location
        direction_to_move = policy_iteration_transitions[current_state]  # returns a direction, e.g. "RIGHT"
        current_state_coords = states_dict[current_state]  # returns a co-ordinate tuple
        if direction_to_move == "TERMINAL":
            print("terminal state reached")
            return True
        elif direction_to_move == "RIGHT":
            new_state_coords = (current_state_coords[0]+1, current_state_coords[1])
        elif direction_to_move == "LEFT":
            new_state_coords = (current_state_coords[0]-1, current_state_coords[1])
        elif direction_to_move == "UP":
            new_state_coords = (current_state_coords[0], current_state_coords[1]+1)
        elif direction_to_move == "DOWN":
            new_state_coords = (current_state_coords[0], current_state_coords[1]-1)
        else:
            print("uh oh")

        # get state number with co-ords new_state_coords
        new_state = list(states_dict.keys())[list(states_dict.values()).index(new_state_coords)]
        print(f"new state coords: {new_state_coords} new state: {new_state}")
        self.move_cell(direction_to_move)
        self._location = new_state
        return False


    def move_cell(self, direction_to_move):
        all_directions = ["UP", "RIGHT", "DOWN", "LEFT"]  # array that will be used circularly for directions
        current_direction = self._facing
        print(f"currently facing: {current_direction}, required: {direction_to_move}")
        while current_direction != direction_to_move:  # turn until facing the required direction of movement

            # if required direction is to the right of current direction
            if all_directions.index(direction_to_move) == (all_directions.index(current_direction) + 1) % 4:
                print("turning right")
                self.left_or_right("RIGHT")  # then move to the right
                current_direction = all_directions[(all_directions.index(current_direction) + 1) % 4]
            else:  # in all other cases, turn left
                print("turning left")
                self.left_or_right("LEFT")
                current_direction = all_directions[(all_directions.index(current_direction) - 1) % 4]

                # inefficient as robot only moves left
                # if current_direction == "UP":
                #     current_direction = "LEFT"
                # elif current_direction == "LEFT":
                #     current_direction = "DOWN"
                # elif current_direction == "DOWN":
                #     current_direction = "RIGHT"
                # elif current_direction == "RIGHT":
                #     current_direction = "UP"
                # else:
                #     print("nopee")

        self._facing = current_direction  # robot is now facing the correct direction so update self._facing
        print(f"now moving: {current_direction}")
        self.forward()

    def left_or_right(self, direction):  # used to turn in the given direction
        set_vel = Twist()

        dict = {"RIGHT" : -2.5, "LEFT" : 2.5}

        # for x in range(2):
        set_vel.linear.x = 0
        set_vel.angular.z = dict[direction]
        r = rospy.Rate(5)
        times = 0
        #
        r.sleep()
        r.sleep()
        for i in range(5):
            self._mover.publish(set_vel) #// we publish the same message many times because otherwise robot will stop
            r.sleep()
        set_vel.angular.z = 0
        self._mover.publish(set_vel)


    def forward(self):
        set_vel = Twist()
        r = rospy.Rate(5)
        speed = 0.5
        set_vel.linear.x = 0.5
        """     
        cell_distance = 5
        current_distance = 0
        t0 = rospy.Time.now().to_sec()
        while(current_distance < cell_distance):
            self._mover.publish(set_vel)
            t1 = rospy.Time.now().to_sec()
            current_distance = speed * (t1-t0)
            r.sleep()
        set_vel.linear.x = 0
        self._mover.publish(set_vel)
        """

        for i in range(35):
            self._mover.publish(set_vel)  # // we publish the same message many times because otherwise robot will stop
            r.sleep()
        set_vel.linear.x = 0
        self._mover.publish(set_vel)

        # r.sleep()

            # set_vel.linear.x = 0.2
        #
        # movement = Twist()
        #
        # # while not rospy.is_shutdown():
        # # # for i in range(1000):
        # #     movement.linear.x = 1
        # #     self._mover.publish(movement)
        # #     # i = i + 1
        # #     # if i == 100000000000:
        # #     #     rospy.signal_shutdown("lols")
        #

        # r = rospy.Rate(100)


        # while not rospy.is_shutdown():
        #     rospy.wait_for_message("/amcl_pose", PoseWithCovarianceStamped, 100)
        #     print(theta)
        #
        #     goal = Point()
        #
        #     print(f"x: {x}, y:{y}")
        #     print(f"goal1{goal}")
        #     goal.x = x + dict[direction][0]
        #     goal.y = y + dict[direction][1]
        #
        #     print(f"goal2{goal}")
        #
        #     x_change = goal.x - x
        #     print(f"x_change{x_change}\n")
        #     y_change = goal.y - y
        #     print(f"y_change{y_change}\n")
        #
        #     angle_to_goal = atan2(y_change, x_change)
        #
        #
        #     print(f"ang = {angle_to_goal}\n")
        #     print(f"theta = {theta}\n")
        #
        #     movement = Twist()
        #
        #     if abs(angle_to_goal - theta) > 0.01:
        #         movement.linear.x = 0.0
        #         movement.angular.z = 0.3
        #     else:
        #         movement.linear.x = 0.5
        #         movement.angular.z = 0.0
        #     self._mover.publish(movement)
        #     print(f"{x_change} and {y_change}\n")

            # r.sleep()

    def send_robot_location(self, coord):
        current_pose = PoseWithCovarianceStamped()
        current_pose.pose.pose.position.x = coord[0]
        current_pose.pose.pose.position.y = coord[1]
        self._robot_publisher.publish(current_pose)
        print("published")



    def check_ingredients(self):

        ## check if the ingredient is out
        # for each ingred in oos
        # is that in the goal state
        # if so - try replaceing that by the next replacement for that ingredient until the replacement is eiter
        # out stock or there are no more replacements

        for ingredient in self._out_of_stock:
            if not self.update_goal(ingredient):
                return False

        return True

    def update_goal(self, ingredient):
        if ingredient in self._goal_ingredients:
            if (not ingredient in self._replacements.keys()):
                return False
            current_ingredient = self._replacements[ingredient]
            # current = replacement
            while (current_ingredient in self._out_of_stock):
                if not current_ingredient in self._replacements.keys():
                    return False
                current_ingredient = self._replacements[current_ingredient]
            for i in range(len(self._goal_ingredients)):
                if current_ingredient == self._goal_ingredients[i]:
                    self._goal_ingredients[i] = current_ingredient
                    break

        return True

    def check_replacement(self, replacement):
        if(replacement[0] + 1 == len(replacement[1])):
            return True
        else:
            return False

    def pick_up_ingredient(self, ingredient, box):
        if not box.can_put_ingredient(ingredient):
            print("Ingredient cannot be found in this box. \n")
            return False
        if not box.check_for_ingredient(ingredient):
            self._out_of_stock.append(ingredient)
            if(not self.update_goal_with_replacement(ingredient)):
                return False
        else:
            self._inventory.append(box.retrieve_ingredient(ingredient))

    def report_impossible_task(self):
        print("Cannot be done")

    def give_ingredients(self, customer):
        customer.receive_ingredients(self._inventory)
        self._inventory = []


if __name__ == '__main__':
    try:
        robot = Robot([], [])

        # robot.move_cell("LEFT")
        # robot.move_cell("LEFT")
        # robot.move_cell("LEFT")
        # robot.move_cell("UP")
        # robot.move_cell("RIGHT")
        # robot.move_cell("LEFT")
        # robot.move_cell("UP")
        # robot.move_cell("DOWN")

        states = {'s0':  (0, 0),  's1': (1, 0),  's2': (2, 0),  's3': (3, 0),  's4': (4, 0),  's5': (5, 0),  's6': (6, 0),  's7': (7, 0),  's8': (8, 0),
              's9':  (1, 1), 's10': (2, 1), 's11': (3, 1), 's12': (5, 1), 's13': (6, 1), 's14': (7, 1), 's15': (8, 1),
              's16': (1, 2), 's17': (2, 2), 's18': (3, 2), 's19': (4, 2), 's20': (5, 2), 's21': (7, 2),
              's22': (1, 3), 's23': (2, 3), 's24': (3, 3), 's25': (4, 3), 's26': (5, 3), 's27': (6, 3), 's28': (7, 3),
              's29': (0, 4), 's30': (1, 4), 's31': (2, 4), 's32': (3, 4), 's33': (5, 4), 's34': (7, 4),
              's35': (1, 5), 's36': (2, 5), 's37': (3, 5), 's38': (4, 5), 's39': (5, 5), 's40': (6, 5), 's41': (7, 5), 's42': (8, 5),
              's43': (0, 6), 's44': (1, 6), 's45': (2, 6), 's46': (3, 6), 's47': (5, 6), 's48': (6, 6), 's49': (7, 6),
              's50': (1, 7), 's51': (3, 7), 's52': (4, 7), 's53': (5, 7), 's54': (7, 7), 's55': (8, 7),
              's56': (0, 8), 's57': (1, 8), 's58': (2, 8), 's59': (3, 8), 's60': (5, 8), 's61': (6, 8), 's62': (7, 8),
              's63': (0, 9), 's64': (1, 9), 's65': (2, 9), 's66': (3, 9), 's67': (4, 9), 's68': (5, 9), 's69': (6, 9), 's70': (7, 9), 's71': (8, 9),
              's72': (0, 10), 's73': (2, 10), 's74': (4, 10), 's75': (7, 10), 's76': (8, 10)}

        pi = {'s0': 'TERMINAL', 's1': 'LEFT', 's2': 'LEFT', 's3': 'LEFT', 's4': 'LEFT', 's5': 'LEFT', 's6': 'TERMINAL', 's7': 'UP', 's8': 'UP', 's9': 'DOWN', 's10': 'LEFT', 's11': 'DOWN', 's12': 'TERMINAL', 's13': 'LEFT', 's14': 'UP', 's15': 'LEFT', 's16': 'DOWN', 's17': 'RIGHT', 's18': 'DOWN', 's19': 'RIGHT', 's20': 'UP', 's21': 'UP', 's22': 'DOWN', 's23': 'LEFT', 's24': 'DOWN', 's25': 'LEFT', 's26': 'UP', 's27': 'RIGHT', 's28': 'UP', 's29': 'RIGHT', 's30': 'DOWN', 's31': 'RIGHT', 's32': 'DOWN', 's33': 'UP', 's34': 'UP', 's35': 'DOWN', 's36': 'LEFT', 's37': 'DOWN', 's38': 'LEFT', 's39': 'LEFT', 's40': 'LEFT', 's41': 'LEFT', 's42': 'LEFT', 's43': 'RIGHT', 's44': 'DOWN', 's45': 'DOWN', 's46': 'DOWN', 's47': 'DOWN', 's48': 'DOWN', 's49': 'DOWN', 's50': 'DOWN', 's51': 'DOWN', 's52': 'LEFT', 's53': 'DOWN', 's54': 'DOWN', 's55': 'LEFT', 's56': 'RIGHT', 's57': 'DOWN', 's58': 'UP', 's59': 'DOWN', 's60': 'DOWN', 's61': 'UP', 's62': 'DOWN', 's63': 'RIGHT', 's64': 'DOWN', 's65': 'LEFT', 's66': 'DOWN', 's67': 'LEFT', 's68': 'DOWN', 's69': 'LEFT', 's70': 'LEFT', 's71': 'LEFT', 's72': 'DOWN', 's73': 'DOWN', 's74': 'DOWN', 's75': 'DOWN', 's76': 'DOWN'}

        for i in range (30):
            if robot.move_using_policy_iteration(states, pi):  # if terminal state reached
                break


        # for i in range(2):
        #    robot.left_or_right("LEFT")

        #
        # # robot.forward()
        # robot.forward()
        #
        # robot.left_or_right("RIGHT")
        # for j in range(5):


        #robot.left_or_right("LEFT")
        # robot.forward()
        #robot.left_or_right("RIGHT")
        #for j in range(5):

        #    robot.forward()

        rospy.spin()
    except rospy.ROSInterruptException:
        pass












