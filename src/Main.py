#!/usr/bin/env python

from Box import Box
from Robot import Robot
from Customer import Customer

def main():

    boxes = []
    boxes.append(Box("Dairy", {"milk": 3, "oat milk": 1, "almond milk": 1}))
    boxes.append(Box("Meat", {"bacon": 2, "pork mince": 1, "ham": 3}))
    boxes.append(Box("Rice", {"jasmine": 1, "basmati": 1, "long grain": 1}))
    boxes.append(Box("Oil", {"sunflower": 2, "olive": 3, "vegetable": 1, "avocado": 0}))

    # the Box.get_available_ingredients() method returns the Box's ingredient dictionary with items and quantities
    # for b in boxes:
    #     print(f"{b.get_name()} : {b.get_available_ingredients()} \n")  # print contents of all boxes
    # print(f"quantity of olive oil: {boxes[3].get_available_ingredients()['olive']} \n")


    replacements = ["milk", "almond milk", "oat milk"]
    #replacements = ["chicken", "cow", "pig", "baby sheep"]

    myRobot = Robot(["milk"], replacements)

    if not myRobot.check_ingredients():
        myRobot.report_impossible_task()

main()



