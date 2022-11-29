#!/usr/bin/env python3

import rospy
from Box import Box
from Robot import Robot
from Customer import Customer
from Shop import Shop
import map, transitions
import os


def main():
    # initialise boxes with ingredients and quantities
    # note: robot also has a list of oos items passed in (for testing) though they may not match quantities below 
    boxes = []
    boxes.append(Box("Dairy", {"milk": 3, "oat milk": 1, "almond milk": 1}))
    boxes.append(Box("Meat", {"bacon": 2, "pork mince": 1, "ham": 3}))
    boxes.append(Box("Rice", {"jasmine": 1, "basmati": 1, "long grain": 1}))
    boxes.append(Box("Oil", {"sunflower": 2, "olive": 3, "vegetable": 1, "avocado": 0}))
    boxes.append(Box("Baking", {"flour": 4, "eggs": 2, "yeast": 1}))
    boxes.append(Box("Nuts", {"almonds": 2, "cashews": 1, "peanuts": 4}))
    boxes.append(Box("Pasta", {"spaghetti": 3, "penne": 2, "lasagne": 1}))
    boxes.append(Box("Fish", {"salmon": 1, "sea bass": 2}))
    boxes.append(Box("Vegetables", {"carrots": 2, "cucumber": 1, "potato": 9}))
    boxes.append(Box("Fruit", {"banana": 4, "apple": 5, "strawberry": 2}))
    boxes.append(Box("Spices", {"paprika": 2, "cumin": 3}))
    boxes.append(Box("Alcohol", {"vodka": 2, "rum": 3}))

    shop = Shop(boxes)

    # create a robot and pass in ingredients and replacements provided by customer
    # TODO: update to make use of Customer class rather than being hard-coded
    goal_ingredients = ["salmon", "spaghetti", "banana"]

    replacements = [["milk", "almond milk", "oat milk"], ["cashews", "almonds"], ["oat milk", "almond milk"]]
    myRobot = Robot(goal_ingredients, replacements)

    myRobot.send_robot_location(map.states()[myRobot.get_location()])

    # replaces oos items and reports impossible task for oos items without replacements
    if not myRobot.check_for_oos_ingredients():  # if any required item is known to be oos and does not have a replacement
        # TODO: if we know that the task is impossible should we still do it? or should we somehow move onto the next customer
        myRobot.report_impossible_task()
    print(f"goal ingredients after replacements: {goal_ingredients} \n")  # prints list of required ingredients after oos items have been replaced

    # get list of states of boxes that the robot needs to visit to pick up all items on the list
    shop.set_boxes_to_visit(goal_ingredients, boxes)
    shop.print_boxes_to_visit()
    
    os.system("say 'hello'&")

    i = 1
    shop.publish_people()
    shop.publish_boxes()
    shop.publish_boxes_to_visit()
    shop.policy_iteration()
    s = "s0"
    while not myRobot.move_using_policy_iteration(map.states(), shop.pi_transitions, shop.transitions, shop.people):  # until a terminal state is reached

        done = False
        if myRobot.check_if_at_box(shop.boxes_to_visit.keys()):  # if the robot is at one of the required boxes

        # TODO: robot actions when it reaches a box
        # robot should pick up items from box here
        # get item if is in the box and has quantity 1+
        # if it is oos then add it to robot oos list and check for replacements
        # if replacement is in this box then try picking it up
        # if it is in another box then add it to the list of boxes to visit
            if (i == 2):
                done = True
                # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n1st")
                # print(shop.transitions)
                # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n2nd")



                shop.set_people(1)


                i = 0

                shop.transitions = transitions.transitions(shop.people)
                print(shop.transitions)
                shop.publish_people()

            shop.update_boxes_to_visit(myRobot.get_location())
            shop.policy_iteration()        # remove box from list of remaining boxes and set its reward back to -1
            shop.print_boxes_to_visit()
            if len(shop.boxes_to_visit) == 0:  # if all boxes have been visited then update policy iteration to return to state 8
                shop.publish_boxes_to_visit()
                shop.set_path_to_customer()
                s = "s8"


        if(i == 2 and done == False):  # TODO: does this always run? is there a better way to implement this?
            print("change\n\n\n\n")

            shop.set_people(1)
            i = 0

            before = transitions.transitions(shop.people)

            shop.transitions = before

            after = transitions.transitions(shop.people)




            shop.policy_iteration()
            shop.publish_people()

        myRobot.send_robot_location(map.states()[myRobot.get_location()])  # send robot location to rviz publisher


        i +=1


        if myRobot.get_location() == s:  # if robot is back in state 8 with the customer, end loop
            print("robot now back at customer")

            # TODO: robot actions when it returns to customer
            # do robot inventory processing here
            # e.g. check whether it matches the customer's ingredient list
            # clear inventory?
            # get new customer?

            break

    print("success!!!!")
    
    
    # TODO: implement a loop around the 'while not' loop so the robot can collect items for back-to-back customers


if __name__ == '__main__':
    rospy.init_node("map_tester")
    main()
    rospy.spin()
