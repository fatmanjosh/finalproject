#!/usr/bin/env python3

import rospy
from Box import Box
from Robot import Robot
from Customer import Customer
from Shop import Shop
import map

def main():
    replacements = ["milk", "almond milk", "oat milk"]
    myRobot = Robot(["milk"], replacements)
    myRobot.send_robot_location(map.states()[myRobot.get_location()])
    boxes = []
    boxes.append(Box("Dairy", {"milk": 3, "oat milk": 1, "almond milk": 1}))
    boxes.append(Box("Meat", {"bacon": 2, "pork mince": 1, "ham": 3}))
    boxes.append(Box("Rice", {"jasmine": 1, "basmati": 1, "long grain": 1}))
    boxes.append(Box("Oil", {"sunflower": 2, "olive": 3, "vegetable": 1, "avocado": 0}))
    boxes.append(Box("Baking", {"flour":4, "eggs": 2, "yeast": 1}))
    boxes.append(Box("Nuts", {"almonds":2, "cashews": 1, "peanuts": 4}))
    boxes.append(Box("Pasta", {"spaghetti": 3, "penne":2, "lasagne": 1}))
    boxes.append(Box("Fish", {"salmon": 1, "sea bass": 2}))
    boxes.append(Box("Vegetables", {"carrots":2, "cucumber": 1, "potato": 9}))
    boxes.append(Box("Fruit", {"banana": 4, "apple": 5, "strawberry": 2}))
    boxes.append(Box("Spices",{"paprika": 2, "cumin": 3}))
    boxes.append(Box("Alcohol", {"vodka": 2, "rum": 3}))
    # the Box.get_available_ingredients() method returns the Box's ingredient dictionary with items and quantities
    # for b in boxes:
    #     print(f"{b.get_name()} : {b.get_available_ingredients()} \n")  # print contents of all boxes
    #print(f"quantity of olive oil: {boxes[3].get_available_ingredients()['olive']} \n")


    #replacements = ["chicken", "cow", "pig", "baby sheep"]




    shop = Shop(boxes)

    if not myRobot.check_ingredients():
        myRobot.report_impossible_task()


    box_count = len(boxes)
    print("hohoho")
    i = 1
    shop.publish_people()
    shop.publish_boxes()
    while not myRobot.move_using_policy_iteration(map.states(), shop.pi_transitions):
        if(i == 1):
            print("change\n\n\n\n")
            shop.heatmap.stateUncertenty(shop.NUM_OF_PEOPLE)
            i = 0
            shop.policy_iteration()
            shop.publish_people()
        # myRobot.markers()
        myRobot.send_robot_location(map.states()[myRobot.get_location()])
        if myRobot.check_if_at_box(shop.get_box_states()):
            shop.update_rewards(myRobot.get_location())
            box_count -= 1
            shop.update_box_states(myRobot.get_location())
            shop.print_box_states()
            if(box_count == 0):
                shop.set_path_to_customer()
        i +=1



        # print(myRobot._location)





if __name__ == '__main__':

    rospy.init_node("map_tester")
    main()
    rospy.spin()


