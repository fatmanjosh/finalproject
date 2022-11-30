#!/usr/bin/env python3

import rospy
from Box import Box
from Robot import Robot
from Customer import Customer
from Shop import Shop
import map, transitions
# import os


def main():
    # initialise boxes with ingredients and quantities
    # note: robot also has a list of oos items passed in (for testing) though they may not match quantities below 
    boxes = []
    boxes.append(Box("Dairy", {"milk": 3, "oat milk": 0, "almond milk": 1}))
    boxes.append(Box("Meat", {"bacon": 2, "pork mince": 1, "ham": 3}))
    boxes.append(Box("Rice", {"jasmine rice": 1, "basmati rice": 1, "long grain rice": 1}))
    boxes.append(Box("Oil", {"sunflower oil": 2, "olive oil": 3, "vegetable oil": 1, "avocado oil": 0}))
    boxes.append(Box("Baking", {"flour": 4, "eggs": 2, "yeast": 1}))
    boxes.append(Box("Nuts", {"almonds": 0, "cashews": 0, "peanuts": 4}))
    boxes.append(Box("Pasta", {"spaghetti": 3, "penne": 2, "lasagne": 1}))
    boxes.append(Box("Fish", {"salmon": 0, "sea bass": 2}))  # TODO: change salmon back to 1
    boxes.append(Box("Vegetables", {"carrots": 2, "cucumber": 1, "potato": 9}))
    boxes.append(Box("Fruit", {"banana": 4, "apple": 5, "strawberry": 2}))
    boxes.append(Box("Spices", {"paprika": 2, "cumin": 3}))
    boxes.append(Box("Alcohol", {"vodka": 2, "rum": 3}))

    shop = Shop(boxes)

    shop._init_markers()

    # create a robot and pass in ingredients and replacements provided by customer
    # TODO: update to make use of Customer class rather than being hard-coded
    goal_ingredients = ["salmon", "carrots", "paprika", "oat milk", "bacon", "basmati rice", "eggs", "cashews", "avocado oil"]
    requested_ingredients = goal_ingredients.copy()
    replacements = [["cashews", "almonds", "peanuts"], ["oat milk", "almond milk"], ["bacon", "ham"], ["avocado oil", "olive oil"]]
    myRobot = Robot(goal_ingredients, replacements)

    myRobot.send_robot_location(map.states()[myRobot.get_location()])

    print(f"\ngoal ingredients : {myRobot.get_goal_ingredients()}")
        
    # replaces oos items and reports impossible task for oos items without replacements
    if not myRobot.check_for_oos_ingredients():  # if any required item is known to be oos and does not have a replacement
        # TODO: if we know that the task is impossible should we still do it? or should we somehow move onto the next customer
        myRobot.report_impossible_task()
        
    print(f"goal ingredients after replacements : {myRobot.get_goal_ingredients()} \n")  # prints list of required ingredients after oos items have been replaced

    # get list of states of boxes that the robot needs to visit to pick up all items on the list
    shop.set_boxes_to_visit(myRobot.get_goal_ingredients(), boxes)
    shop.print_boxes_to_visit()
        
    # add people and boxes to rviz
    shop.publish_people()
    shop.publish_boxes()
    shop.publish_boxes_to_visit()
    shop.policy_iteration()
    shop.post_start_customer()
    
    i = 1
    while not myRobot.move_using_policy_iteration(map.states(), shop.pi_transitions, shop.transitions, shop.people):  # until a terminal state is reached
        
        myRobot.send_robot_location(map.states()[myRobot.get_location()])  # update robot's pose for rviz
        done = False
        
        if myRobot.check_if_at_box(shop.boxes_to_visit.keys()):            # if the robot is at one of the required boxes
            
            if (i == 2):
                done = True
                shop.set_people(1)
                
                i = 0

                shop.transitions = transitions.transitions(shop.people)
                print(shop.transitions)
                shop.publish_people()
            
            # get the box at our current state
            for box in boxes:
                if str(box.get_name()) == str(shop.box_states[myRobot.get_location()]):
                    myRobot.current_box = box  
                    break
            
            print("---------------------------------------------------------------------------")    
            print(f"contents of current box : {myRobot.current_box.get_available_ingredients()}")
            
            # picks up all goal ingredients contained within this box
            myRobot.pick_up_all_required_ingredients_from_box()
            
            # print out robot inventory and contents of box after robot picks up ingredients
            print(f"\nrobot inventory : {myRobot.get_inventory()}")
            print(f"updated box contents: {myRobot.current_box.get_available_ingredients()}")               

            # update boxes to visit in case any new ones were added, e.g. if an item was oos and replacement is in another box
            shop.set_boxes_to_visit(myRobot.get_goal_ingredients(), boxes)  
            
            shop.update_boxes_to_visit(myRobot.get_location())  # remove box from list of remaining boxes and set its reward back to -1
            shop.print_boxes_to_visit()  # print the list of remaining boxes to visit
                        
            
            if len(shop.boxes_to_visit) == 0:  # if all boxes have been visited then update policy iteration to return to state 8
                shop.publish_boxes_to_visit()
                shop.set_path_to_customer()
                shop.post_end_customer()

                
        if(i == 2 and done == False):  # TODO: does this always run? is there a better way to implement this?
            # print("change\n\n\n\n")
            shop.set_people(1)
            i = 0

            before = transitions.transitions(shop.people)

            shop.transitions = before

            after = transitions.transitions(shop.people)

            shop.policy_iteration()
            shop.publish_people()

        myRobot.send_robot_location(map.states()[myRobot.get_location()])  # send robot location to rviz publisher
            
        i += 1    
        
        if myRobot.get_location() == "s8":  # if robot is back in state 8 with the customer, end loop
            print("robot now back at customer \n")

            # sort lists alphabetically for readability and then print them 
            requested_ingredients.sort()
            myRobot.get_inventory().sort()
            
            print(f"ingredients requested by customer : {requested_ingredients}")
            print(f"ingredients returned by the robot : {myRobot.get_inventory()}")
            # print(f"unavailable items : {unavailable_items} \n")
            print(f"substitutions : {myRobot.get_substitutions()}")
            print(f"unavailable : {myRobot.get_unavailable()}")

            # TODO: robot actions when it returns to customer
            # do robot inventory processing here
            # e.g. check whether it matches the customer's ingredient list
            # clear inventory?
            # get new customer?            

            break
        
    print("\nsuccess!!!!")
    
    
    # TODO: implement a loop around the 'while not' loop so the robot can collect items for back-to-back customers


if __name__ == '__main__':
    rospy.init_node("map_tester")
    main()
    rospy.spin()
