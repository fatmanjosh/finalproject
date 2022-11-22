import math

import rospy
from geometry_msgs.msg import Twist, Point, PoseWithCovarianceStamped
from math import atan2, pi
from nav_msgs.msg import Odometry

class Robot:
    def __init__(self, goal_ingredients, replacements):
        self._mover = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self._initialiser = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=10)
        self._listener = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.newOdom)
        rospy.init_node('mover', anonymous=True)
        self._goal_ingredients = goal_ingredients
        self._inventory = []
        self._out_of_stock = ["milk", "almond milk"]
        self._replacements = self.update_food_dictionary(replacements)
        self._facing = "RIGHT"
        self.location = "s8"

        # oat milk : almond milk -- mapping oat to almond as an alternative

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
        print(f"theta{theta}")

        print("\n\n\n\n looooooooool \n\n\n\n\n\n")
    def left_or_right(self, direction):
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

        set_vel.linear.x = 0.5
        set_vel.angular.z = 0
        times = 0
        # r.sleep()
        # r.sleep()
        r.sleep()
        self._mover.publish(set_vel)  # // we publish the same message many times because otherwise robot will stop
        r.sleep()
        set_vel.linear.x = 0
        self._mover.publish(set_vel)

        # for x in range(2):
        set_vel.linear.x = 5
        # set_vel.angular.z = 0
        # r = rospy.Rate(5)
        times = 0
        #
        # r.sleep()
        # r.sleep()
        r.sleep()
        for i in range(17):
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
        robot = Robot([],[])
        for i in range(2):
            robot.left_or_right("LEFT")

        robot.forward()

        robot.left_or_right("RIGHT")
        for j in range(5):
            robot.forward()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

