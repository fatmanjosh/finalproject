#!/usr/bin/env python3

import math
from time import perf_counter_ns
import rospy
from geometry_msgs.msg import Twist, Point, PoseStamped, Pose
from math import atan2, pi
from nav_msgs.msg import Odometry


from geometry_msgs.msg import Quaternion
from visualization_msgs.msg import MarkerArray, Marker


class Robot:
    def __init__(self, goal_ingredients, replacements):

        self._mover = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self._robot_publisher = rospy.Publisher('/robot_location', PoseStamped)

        # self._listener = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.newOdom)
        # rospy.init_node('mover', anonymous=True)
        self._goal_ingredients = goal_ingredients
        self._inventory = []
        self._out_of_stock = ["milk", "almond milk"]
        self._replacements = self.update_food_dictionary(replacements)
        self._facing = "RIGHT"
        self._location = "s8"
        self.current_pose = PoseStamped()

        self.mark_pub = rospy.Publisher('/marker', Marker, queue_size=10)



        # oat milk : almond milk -- mapping oat to almond as an alternative

    # def check_if_at_box(self):
    #     if

    def get_location(self):
        return self._location

    def markers(self):
        marker = Marker()
        # marker.pose = self.current_pose.pose
        marker.header.frame_id = "/map"
        marker.id = 0
        marker.pose.position.x = 10
        marker.pose.position.y = 10

        marker.type = marker.CYLINDER
        marker.action = 2
        marker.color.r = 1
        marker.color.g = 1
        marker.color.b = 0.0
        marker.color.a = 1
        marker.scale.x = 10
        marker.scale.y = 10
        marker.scale.z = 100
        marker.frame_locked = True
        marker.ns = "Goal"

        self.mark_pub.publish(marker)

    # def move_with_probability(self):
    #

    def check_if_at_box(self, box_states):
        if (self._location in box_states):
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
            new_state_coords = (current_state_coords[0] + 1, current_state_coords[1])
        elif direction_to_move == "LEFT":
            new_state_coords = (current_state_coords[0] - 1, current_state_coords[1])
        elif direction_to_move == "UP":
            new_state_coords = (current_state_coords[0], current_state_coords[1] + 1)
        elif direction_to_move == "DOWN":
            new_state_coords = (current_state_coords[0], current_state_coords[1] - 1)
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
                # self.send_robot_location()
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

        toTurn = {"RIGHT": -2.5, "LEFT": 2.5}
        current_direction = {"LEFT": (-0.2, 0), "RIGHT": (0.2, 0), "UP": (0, 0.2), "DOWN": (0, -0.2)}

        howToMOve = {"LEFT" : {"RIGHT" : (-0.2, -0.4, "UP"), "LEFT" : (0.2, -0.4, "DOWN")},
                     "RIGHT": {"RIGHT" : (0.4, -0.2, "DOWN"), "LEFT" : (0, -0.2, "UP")},
                     "UP"   : {"RIGHT" : (0, 0.2, "RIGHT"),   "LEFT" : (0.2, 0.4, "LEFT")},
                     "DOWN" : {"RIGHT" : (-0.2, -0.4, "LEFT"),"LEFT" : (-0.4, 0.2, "RIGHT")}
                     }

        # if (self._facing == "RIGHT"):
        #     self.current_pose.pose.orientation.w = -1
        #     self.current_pose.pose.orientation.z = 0
        # elif (self._facing == "LEFT"):
        #     self.current_pose.pose.orientation.w = 0
        #     self.current_pose.pose.orientation.z = 1
        # elif (self._facing == "UP"):
        #     self.current_pose.pose.orientation.w = -1
        #     self.current_pose.pose.orientation.z = -1
        # else:
        #     self.current_pose.pose.orientation.w = 1
        #     self.current_pose.pose.orientation.z = -1

        # for x in range(2):
        set_vel.linear.x = 0
        set_vel.angular.z = toTurn[direction]
        r = rospy.Rate(5)
        times = 0
        #
        r.sleep()
        r.sleep()
        for i in range(5):
            self.current_pose.pose.orientation.w += howToMOve[self._facing][direction][0]
            self.current_pose.pose.orientation.z += howToMOve[self._facing][direction][1]
            print(f"w:{self.current_pose.pose.orientation.w} z:{self.current_pose.pose.orientation.z}")
            self._mover.publish(set_vel)
            r.sleep()
            self._robot_publisher.publish(self.current_pose)
            # self.marker[0].id += 1
            # self.mark_pub.publish(self.marker)# // we publish the same message many times because otherwise robot will stop
        self._facing = howToMOve[self._facing][direction][2]
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
            self.move_robot_pose_forward()
        set_vel.linear.x = 0
        self._mover.publish(set_vel)

    def move_robot_pose_forward(self):
        dict = {"LEFT" : (-0.2, 0), "RIGHT" : (0.2, 0),"UP" : (0, 0.2),"DOWN" : (0, -0.2)}
        self.current_pose.pose.position.x += dict[self._facing][0]
        self.current_pose.pose.position.y += dict[self._facing][1]
        self._robot_publisher.publish(self.current_pose)


    def send_robot_location(self, coord):
        print(self._facing)
        if (self._facing == "RIGHT"):
            self.current_pose.pose.orientation.w = -1
            self.current_pose.pose.orientation.z = 0
        elif (self._facing == "LEFT"):
            self.current_pose.pose.orientation.w = 0
            self.current_pose.pose.orientation.z = 1
        elif (self._facing == "UP"):
            self.current_pose.pose.orientation.w = -1
            self.current_pose.pose.orientation.z = -1
        else:
            self.current_pose.pose.orientation.w = 1
            self.current_pose.pose.orientation.z = -1


        print(f"orientation{self.current_pose.pose.orientation}")


        self.current_pose.pose.position.x = coord[0] * 7 + 4
        self.current_pose.pose.position.y = coord[1] * 7 + 4
        print(f"x: {coord[0] * 7 + 4} y : {coord[1] * 7 + 4}")
        self.current_pose.header.frame_id = "map"
        self._robot_publisher.publish(self.current_pose)
        print("published")

        # print(current_pose.header)

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
        if (replacement[0] + 1 == len(replacement[1])):
            return True
        else:
            return False

    def pick_up_ingredient(self, ingredient, box):
        if not box.can_put_ingredient(ingredient):
            print("Ingredient cannot be found in this box. \n")
            return False
        if not box.check_for_ingredient(ingredient):
            self._out_of_stock.append(ingredient)
            if (not self.update_goal_with_replacement(ingredient)):
                return False
        else:
            self._inventory.append(box.retrieve_ingredient(ingredient))

    def report_impossible_task(self):
        print("Cannot be done")

    def give_ingredients(self, customer):
        customer.receive_ingredients(self._inventory)
        self._inventory = []

    def rotateQuaternion(self, q_orig, yaw):
        """
        Converts a basic rotation about the z-axis (in radians) into the
        Quaternion notation required by ROS transform and pose messages.

        :Args:
           | q_orig (geometry_msgs.msg.Quaternion): to be rotated
           | yaw (double): rotate by this amount in radians
        :Return:
           | (geometry_msgs.msg.Quaternion) q_orig rotated yaw about the z axis
         """
        # Create a temporary Quaternion to represent the change in heading
        print(f"yaw - {yaw}")

        q_headingChange = Quaternion()

        p = 0
        y = yaw / 2.0
        r = 0

        sinp = math.sin(p)
        siny = math.sin(y)
        sinr = math.sin(r)
        cosp = math.cos(p)
        cosy = math.cos(y)
        cosr = math.cos(r)

        q_headingChange.x = sinr * cosp * cosy - cosr * sinp * siny
        q_headingChange.y = cosr * sinp * cosy + sinr * cosp * siny
        q_headingChange.z = cosr * cosp * siny - sinr * sinp * cosy
        q_headingChange.w = cosr * cosp * cosy + sinr * sinp * siny

        # ----- Multiply new (heading-only) quaternion by the existing (pitch and bank)
        # ----- quaternion. Order is important! Original orientation is the second
        # ----- argument rotation which will be applied to the quaternion is the first
        # ----- argument.
        return self.multiply_quaternions(q_headingChange, q_orig)

    def multiply_quaternions(self, qa, qb):
        """
        Multiplies two quaternions to give the rotation of qb by qa.

        :Args:
           | qa (geometry_msgs.msg.Quaternion): rotation amount to apply to qb
           | qb (geometry_msgs.msg.Quaternion): to rotate by qa
        :Return:
           | (geometry_msgs.msg.Quaternion): qb rotated by qa.
        """
        combined = Quaternion()

        combined.w = (qa.w * qb.w - qa.x * qb.x - qa.y * qb.y - qa.z * qb.z)
        combined.x = (qa.x * qb.w + qa.w * qb.x + qa.y * qb.z - qa.z * qb.y)
        combined.y = (qa.w * qb.y - qa.x * qb.z + qa.y * qb.w + qa.z * qb.x)
        combined.z = (qa.w * qb.z + qa.x * qb.y - qa.y * qb.x + qa.z * qb.w)
        return combined


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

        states = {'s0': (0, 0), 's1': (1, 0), 's2': (2, 0), 's3': (3, 0), 's4': (4, 0), 's5': (5, 0), 's6': (6, 0),
                  's7': (7, 0), 's8': (8, 0),
                  's9': (1, 1), 's10': (2, 1), 's11': (3, 1), 's12': (5, 1), 's13': (6, 1), 's14': (7, 1),
                  's15': (8, 1),
                  's16': (1, 2), 's17': (2, 2), 's18': (3, 2), 's19': (4, 2), 's20': (5, 2), 's21': (7, 2),
                  's22': (1, 3), 's23': (2, 3), 's24': (3, 3), 's25': (4, 3), 's26': (5, 3), 's27': (6, 3),
                  's28': (7, 3),
                  's29': (0, 4), 's30': (1, 4), 's31': (2, 4), 's32': (3, 4), 's33': (5, 4), 's34': (7, 4),
                  's35': (1, 5), 's36': (2, 5), 's37': (3, 5), 's38': (4, 5), 's39': (5, 5), 's40': (6, 5),
                  's41': (7, 5), 's42': (8, 5),
                  's43': (0, 6), 's44': (1, 6), 's45': (2, 6), 's46': (3, 6), 's47': (5, 6), 's48': (6, 6),
                  's49': (7, 6),
                  's50': (1, 7), 's51': (3, 7), 's52': (4, 7), 's53': (5, 7), 's54': (7, 7), 's55': (8, 7),
                  's56': (0, 8), 's57': (1, 8), 's58': (2, 8), 's59': (3, 8), 's60': (5, 8), 's61': (6, 8),
                  's62': (7, 8),
                  's63': (0, 9), 's64': (1, 9), 's65': (2, 9), 's66': (3, 9), 's67': (4, 9), 's68': (5, 9),
                  's69': (6, 9), 's70': (7, 9), 's71': (8, 9),
                  's72': (0, 10), 's73': (2, 10), 's74': (4, 10), 's75': (7, 10), 's76': (8, 10)}

        pi = {'s0': 'TERMINAL', 's1': 'LEFT', 's2': 'LEFT', 's3': 'LEFT', 's4': 'LEFT', 's5': 'LEFT', 's6': 'TERMINAL',
              's7': 'UP', 's8': 'UP', 's9': 'DOWN', 's10': 'LEFT', 's11': 'DOWN', 's12': 'TERMINAL', 's13': 'LEFT',
              's14': 'UP', 's15': 'LEFT', 's16': 'DOWN', 's17': 'RIGHT', 's18': 'DOWN', 's19': 'RIGHT', 's20': 'UP',
              's21': 'UP', 's22': 'DOWN', 's23': 'LEFT', 's24': 'DOWN', 's25': 'LEFT', 's26': 'UP', 's27': 'RIGHT',
              's28': 'UP', 's29': 'RIGHT', 's30': 'DOWN', 's31': 'RIGHT', 's32': 'DOWN', 's33': 'UP', 's34': 'UP',
              's35': 'DOWN', 's36': 'LEFT', 's37': 'DOWN', 's38': 'LEFT', 's39': 'LEFT', 's40': 'LEFT', 's41': 'LEFT',
              's42': 'LEFT', 's43': 'RIGHT', 's44': 'DOWN', 's45': 'DOWN', 's46': 'DOWN', 's47': 'DOWN', 's48': 'DOWN',
              's49': 'DOWN', 's50': 'DOWN', 's51': 'DOWN', 's52': 'LEFT', 's53': 'DOWN', 's54': 'DOWN', 's55': 'LEFT',
              's56': 'RIGHT', 's57': 'DOWN', 's58': 'UP', 's59': 'DOWN', 's60': 'DOWN', 's61': 'UP', 's62': 'DOWN',
              's63': 'RIGHT', 's64': 'DOWN', 's65': 'LEFT', 's66': 'DOWN', 's67': 'LEFT', 's68': 'DOWN', 's69': 'LEFT',
              's70': 'LEFT', 's71': 'LEFT', 's72': 'DOWN', 's73': 'DOWN', 's74': 'DOWN', 's75': 'DOWN', 's76': 'DOWN'}

        for i in range(30):
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

        # robot.left_or_right("LEFT")
        # robot.forward()
        # robot.left_or_right("RIGHT")
        # for j in range(5):

        #    robot.forward()

        rospy.spin()
    except rospy.ROSInterruptException:
        pass
